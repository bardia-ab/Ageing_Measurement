from resources.clock_manager import CM
from resources.data_process import *
import matplotlib.pyplot as plt
import time, math

start_time = time.time()
ila_path = r'C:\Users\t26607bb\Desktop\CPS_Project\Vivado_Projects\CPS_Single\Results'

MMCM1 = CM(fin=100e6, D=1, M=15, O=15, mode='incremental', fpsclk=100e6)
MMCM2 = CM(fin=MMCM1.fout, D=1, M=16, O=16, mode='decremental', fpsclk=100e6)
MMCM3 = CM(fin=MMCM1.fout, D=1, M=16, O=16)
N_Parallel = 50

T = 1 / MMCM2.fout
N_Sets = MMCM1.fvco // (MMCM2.fvco - MMCM1.fvco)
N_Samples = 56 * MMCM2.O * N_Sets / 2
w_shift = math.ceil(math.log2(N_Samples))
N_Bytes = math.ceil((w_shift + N_Parallel) / 8)
sps = MMCM2.sps / N_Sets

txt_file = os.path.join(r'C:\Users\t26607bb\Desktop', 'Tx.txt')
chars = pack_data(txt_file, N_Bytes)
shift_values, CUT_indexes = decompose_shift_capture(chars, w_shift, N_Parallel)
segments = extract_delays(shift_values, CUT_indexes, sps)


print('--- %s seconds ---' %(time.time() - start_time))