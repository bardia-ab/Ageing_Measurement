import time, os, re
from itertools import count
from resources.data_process import create_folder, store_data

start_time = time.time()
bitstream_path = '/home/bardia/Desktop/bardia/Timing_Characterization/Data_xczu9eg/Bitstreams/X3Y0'  #program
results_path = '/home/bardia/Desktop/bardia/Timing_Characterization/Data_xczu9eg/Results/X3Y0'       #store
srcs_path = '/home/bardia/Desktop/bardia/Timing_Characterization/Data_xczu9eg/Vivado_Sources_local/X3Y0'   #validation
create_folder(results_path)
with open (os.path.join(results_path, 'Errors.txt'), 'w') as file1:
    pass

with open (os.path.join(results_path, 'validation.txt'), 'w') as file2:
    pass

baud_rate = 230400
COM_port = '/dev/ttyUSB0'
N_Parallel = 50
N_Errors = count(start=1)

bitstreams = [file for file in os.listdir(bitstream_path) if file.startswith('TC')]
TCs = sorted(bitstreams, key= lambda x: int(re.findall('\d+', x)[0]))
for TC in TCs:
    TC_idx = TC.split('.')[0]
    try:
        os.system(f'python3 ManAge.py {N_Parallel} {COM_port} {baud_rate} {TC_idx} {bitstream_path} {results_path} {srcs_path}')
    except:
        print(f'{N_Errors}- TC{TC_idx}')

    files = list(filter(lambda x: x.startswith('vivado'), os.listdir(os.getcwd())))
    for file in files:
        os.remove(file)

print('--- %s seconds ---' %(time.time() - start_time))