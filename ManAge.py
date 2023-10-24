import sys, os, threading
import time, serial, math
from resources.clock_manager import CM
from resources.data_process import *

######################################
class Read:

    def __init__(self):
        self.packet = None
    def read_data(self, port):
        self.packet = port.read_until(b'END')


############ User Inputs ##############
N_Parallel      = int(sys.argv[1])
COM_port        = sys.argv[2]
baud_rate       = int(sys.argv[3])
TC_idx          = sys.argv[4]
bitstream_path  = sys.argv[5]
store_path      = sys.argv[6]
srcs_path       = sys.argv[7]
os.system(f'vivado -mode batch -nolog -nojournal -source ./program.tcl -tclargs "{bitstream_path}" "{TC_idx}"')
time.sleep(10)
############ MMCM Initialization ##############
MMCM1 = CM(fin=100e6, D=1, M=15, O=15, mode='incremental', fpsclk=100e6)
MMCM2 = CM(fin=MMCM1.fout, D=1, M=16, O=16, mode='decremental', fpsclk=100e6)
MMCM3 = CM(fin=MMCM1.fout, D=1, M=16, O=16)

T = 1 / MMCM2.fout
N_Sets = MMCM1.fvco // (MMCM2.fvco - MMCM1.fvco)
N_Samples = 56 * MMCM2.O * N_Sets / 2
w_shift = math.ceil(math.log2(N_Samples))
N_Bytes = math.ceil((w_shift + N_Parallel) / 8)
sps = MMCM2.sps / N_Sets

############ Run Experiment ##############
port = serial.Serial(COM_port, baud_rate, timeout=220)
R = Read()
T1 = threading.Thread(target=Read.read_data, args=(R, port))
T2 = threading.Thread(target=Read.read_data, args=(R, port))
port.flushInput()
print(port.name)
data_rising, data_falling = [], []

port.write('RUS'.encode('Ascii'))
#packet = port.read_until(b'END')
T1.start()
T1.join()
packet = R.packet
data_rising += list(packet[:-3])

port.write('RDS'.encode('Ascii'))
#packet = port.read_until(b'END')
T2.start()
T2.join()
packet = R.packet
data_falling += list(packet[:-3])
port.write('R'.encode('Ascii'))

port.close()

############ Processing ##############
TC_folder_path = os.path.join(store_path, f'{TC_idx}')
create_folder(TC_folder_path)

while 1:
    try:
        chars = pack_bytes(data_rising, N_Bytes)
        shift_values, CUT_indexes = decompose_shift_capture(chars, w_shift, N_Parallel)
        segments_rising = extract_delays(shift_values, CUT_indexes, N_Parallel, sps)
        store_data(TC_folder_path, 'segments_rising.data', segments_rising)
    except:
        with open(os.path.join(store_path, 'Errors.txt'), 'a+') as file:
            file.write(f'{TC_idx} => Rising Failed!\n')

        break

    if not validate_result(segments_rising, srcs_path, TC_idx, N_Parallel):
        with open(os.path.join(store_path, 'validation.txt'), 'a+') as file:
            file.write(f'{TC_idx} => Rising Failed!\n')
    else:
        print(f'{TC_idx} => Rising Passed!\n')

    try:
        chars = pack_bytes(data_falling, N_Bytes)
        shift_values, CUT_indexes = decompose_shift_capture(chars, w_shift, N_Parallel)
        segments_falling = extract_delays(shift_values, CUT_indexes, N_Parallel, sps)
        store_data(TC_folder_path, 'segments_falling.data', segments_falling)
    except:
        with open(os.path.join(store_path, 'Errors.txt'), 'a+') as file:
            file.write(f'{TC_idx} => Falling Failed!\n')

        break

    if not validate_result(segments_falling, srcs_path, TC_idx, N_Parallel):
        with open(os.path.join(store_path, 'validation.txt'), 'a+') as file:
            file.write(f'{TC_idx} => Falling Failed!\n')
    else:
        print(f'{TC_idx} => Falling Passed!\n')

    break