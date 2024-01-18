import time, os, shutil
from resources.data_process import create_folder
start_time = time.time()

Src_Dir = r'/home/bardia/Desktop/bardia/Timing_Characterization/Data/Vivado_Sources'
Proj_Dir = r'/home/bardia/Desktop/bardia/FPGA_Projects/CPS_Parallel_ZCU9'
Store_path = r'/home/bardia/Desktop/bardia/Timing_Characterization/Data'
DLOC_path = os.path.join(Store_path, 'DLOC_dicts')
load_path = os.path.join(Store_path, 'Load')
result_path = os.path.join(Store_path, 'Results')
bitstream_path = os.path.join(Store_path, 'Bitstreams')

TCs = set()
files = ['Errors.txt', 'validation.txt']
for file in files:
    with open(os.path.join(result_path, file)) as txt:
        for line in txt.readlines():
            if line == '\n':
                continue

            TC = line.split(' => ')[0]
            TCs.add(TC)

baud_rate = 230400
COM_port = '/dev/ttyUSB0'
N_Parallel = 50
for TC in TCs:
    os.system(f'python3 ManAge.py {N_Parallel} {COM_port} {baud_rate} {TC} {bitstream_path} {result_path} {Src_Dir}')


print('--- %s seconds ---' %(time.time() - start_time))