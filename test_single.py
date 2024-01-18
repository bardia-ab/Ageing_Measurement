import os
from resources.data_process import load_data

baud_rate = 230400
COM_port = '/dev/ttyUSB0'
N_Parallel = 50

TCs_idx = ['TC1']
bitstream_path2 = f'/home/bardia/Desktop/bardia/Timing_Characterization/Data_xczu9eg/Bitstreams'   #program
results_path2 = f'/home/bardia/Desktop/bardia/Timing_Characterization/Data_xczu9eg/Results'         #store
srcs_path2 = f'/home/bardia/Desktop/bardia/Timing_Characterization/Data_xczu9eg/Vivado_Sources_local' #validation

for CR in ['X3Y0']:
#for CR in os.listdir(bitstream_path2):
    bitstream_path = os.path.join(bitstream_path2, CR)  # program
    results_path = os.path.join(results_path2, CR)  # store
    srcs_path = os.path.join(srcs_path2, CR) # validation
    '''file = open(os.path.join(results_path, 'Errors.txt'), 'w+')
    file = open(os.path.join(results_path, 'validation.txt'), 'w+')

    TCs_idx = [file.split('.')[0] for file in os.listdir(bitstream_path) if '_' in file]'''
    #srcs_path = os.path.join(srcs_path, 'Split_Sources')

    for TC_idx in TCs_idx:
        os.system(f'python3 ManAge.py {N_Parallel} {COM_port} {baud_rate} {TC_idx} {bitstream_path} {results_path} {srcs_path}')

'''store_path = os.path.join(results_path, TC_idx)
for file in os.listdir(store_path):
    segment = load_data(store_path, file)
    pass'''