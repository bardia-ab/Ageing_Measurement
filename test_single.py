import os
from resources.data_process import load_data

baud_rate = 230400
COM_port = '/dev/ttyUSB2'
N_Parallel = 50
TC_idx = 'TC38'

bitstream_path = '/home/bardia/Desktop/bardia/Timing_Characterization/Data/Bitstreams'  #program
#bitstream_path = '/home/bardia/Desktop/bardia/FPGA_Projects/CPS_Parallel_ZCU9/CPS_Parallel_ZCU9.runs/impl_1'  #program
results_path = '/home/bardia/Desktop/bardia/Timing_Characterization/Data/Results'       #store
#srcs_path = '/home/bardia/Desktop/bardia/Timing_Characterization/Data/test/Failed' #validation
srcs_path = '/home/bardia/Desktop/bardia/Timing_Characterization/Data/Vivado_Sources' #validation



os.system(f'python3 ManAge.py {N_Parallel} {COM_port} {baud_rate} {TC_idx} {bitstream_path} {results_path} {srcs_path}')

store_path = os.path.join(results_path, TC_idx)
for file in os.listdir(store_path):
    segment = load_data(store_path, file)
    pass