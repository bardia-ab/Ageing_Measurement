import time, os, shutil
from itertools import count
from resources.data_process import create_folder, store_data

start_time = time.time()
bitstream_path = '/home/bardia/Desktop/bardia/Timing_Characterization/Data/test/Bitstreams'  #program
results_path = '/home/bardia/Desktop/bardia/Timing_Characterization/Data/test'       #store
srcs_path = '/home/bardia/Desktop/bardia/Timing_Characterization/Data/Vivado_Sources' #validation
Proj_Dir = '/home/bardia/Desktop/bardia/FPGA_Projects/CPS_Parallel_ZCU9'
failed_path = os.path.join(results_path, 'Failed')
#create_folder(results_path)
#create_folder(failed_path)
#create_folder(bitstream_path)
#create_folder(os.path.join(results_path, 'DCPs'))
create_folder(os.path.join(results_path, 'Logs'))
with open (os.path.join(results_path, 'Errors.txt'), 'w') as file1:
    pass

with open (os.path.join(results_path, 'validation.txt'), 'w') as file2:
    pass

baud_rate = 230400
COM_port = '/dev/ttyUSB0'
N_Parallel = 50
N_Errors = count(start=1)

with open('/home/bardia/Desktop/bardia/Timing_Characterization/Data/Results/validation.txt') as file:
    validation_file = file.readlines()

TCs = {line.split(' =>')[0] for line in validation_file}
'''for TC in TCs:
    src = os.path.join(srcs_path, TC)
    dst = os.path.join(failed_path, TC)
    shutil.copytree(src, dst)

os.system(
        f'vivado -mode batch -nolog -nojournal -source /home/bardia/Desktop/Path_Search/tcl_sources/gen_bit.tcl -tclargs "{failed_path}" "{Proj_Dir}" "{results_path}" "0" "{50}" "{N_Parallel}" "custom"')'''
#TCs = 20 * ['TC5.bit']
for TC in TCs:
    TC_idx = TC.split('.')[0]
    try:
        os.system(f'python3 ManAge.py {N_Parallel} {COM_port} {baud_rate} {TC_idx} {bitstream_path} {results_path} {failed_path}')
    except:
        print(f'{N_Errors}- TC{TC_idx}')

    files = list(filter(lambda x: x.startswith('vivado'), os.listdir(os.getcwd())))
    for file in files:
        os.remove(file)

print('--- %s seconds ---' %(time.time() - start_time))