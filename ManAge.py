import sys, os
import time, serial, math
from resources.clock_manager import CM
from resources.data_process import *

############ User Inputs ##############
N_Parallel  = int(sys.argv[1])
COM_port    = sys.argv[2]
baud_rate   = int(sys.argv[3])
TC_idx     = sys.argv[4]
store_path  = sys.argv[5]
os.system(f'vivado -mode batch -source ./program.tcl -tclargs "{TC_idx}"')

############ MMCM Initialization ##############
MMCM1 = CM(fin=100e6, D=1, M=15, O=15, mode='incremental', fpsclk=100e6)
MMCM2 = CM(fin=MMCM1.fout, D=1, M=16, O=16, mode='decremental', fpsclk=100e6)
MMCM3 = CM(fin=MMCM1.fout, D=1, M=16, O=16)
#N_Parallel = 50

T = 1 / MMCM2.fout
N_Sets = MMCM1.fvco // (MMCM2.fvco - MMCM1.fvco)
N_Samples = 56 * MMCM2.O * N_Sets / 2
w_shift = math.ceil(math.log2(N_Samples))
N_Bytes = math.ceil((w_shift + N_Parallel) / 8)
sps = MMCM2.sps / N_Sets

############ Run Experiment ##############
port = serial.Serial(COM_port, baud_rate)
port.flushInput()
print(port.name)
data_rising, data_falling = [], []

port.write('RUS'.encode('Ascii'))
packet = port.read_until(b'END')
data_rising += list(packet[:-3])

port.write('RDS'.encode('Ascii'))
packet = port.read_until(b'END')
data_falling += list(packet[:-3])

port.close()

############ Processing ##############
store_path = os.path.join(store_path, f'TC{TC_idx}')
create_folder(store_path)

chars = pack_bytes(data_rising, N_Bytes)
shift_values, CUT_indexes = decompose_shift_capture(chars, w_shift, N_Parallel)
segments_rising = extract_delays(shift_values, CUT_indexes, sps)
store_data(store_path, 'segments_rising.data', segments_rising)

chars = pack_bytes(data_falling, N_Bytes)
shift_values, CUT_indexes = decompose_shift_capture(chars, w_shift, N_Parallel)
segments_falling = extract_delays(shift_values, CUT_indexes, sps)
store_data(store_path, 'segments_falling.data', segments_falling)
