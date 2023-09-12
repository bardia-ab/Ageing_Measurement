import time, os, re
from itertools import count
from resources.data_process import create_folder, store_data

start_time = time.time()
bitstream_path = '/home/bardia/Desktop/bardia/Timing_Characterization/Data/Bitstreams'
results_path = '/home/bardia/Desktop/bardia/Timing_Characterization/Data/Results'
srcs_path = '/home/bardia/Desktop/bardia/Timing_Characterization/Data/Vivado_Sources'
create_folder(results_path)
with open (os.path.join(results_path, 'Errors.txt'), 'w') as file:
    pass

with open (os.path.join(results_path, 'validation.txt'), 'w') as file:
    pass

baud_rate = 230400
COM_port = '/dev/ttyUSB0'
N_Parallel = 50
N_Errors = count(start=1)
Errors = []

#os.system(f'python3 ManAge.py {N_Parallel} {COM_port} {baud_rate} {157} {results_path} {srcs_path}')
for TC in os.listdir(bitstream_path):
    TC_idx = re.search('\d+', TC)[0]
    try:
        os.system(f'python3 ManAge.py {N_Parallel} {COM_port} {baud_rate} {TC_idx} {results_path} {srcs_path}')
    except:
        print(f'{N_Errors}- TC{TC_idx}')
        Errors.append(TC_idx)

    files = list(filter(lambda x: x.startswith('vivado'), os.listdir(os.getcwd())))
    for file in files:
        os.remove(file)

store_data(results_path, 'Errors.data', Errors)
print('--- %s seconds ---' %(time.time() - start_time))