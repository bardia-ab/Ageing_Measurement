from resources.clock_manager import CM
from resources.data_process import *
import matplotlib.pyplot as plt
import time

start_time = time.time()
#ila_path = r'C:\Users\t26607bb\Desktop'

MMCM1 = CM(fin=100e6, D=1, M=15, O=15, mode='incremental', fpsclk=100e6)
MMCM2 = CM(fin=MMCM1.fout, D=1, M=16, O=16, mode='decremental', fpsclk=100e6)
MMCM3 = CM(fin=MMCM1.fout, D=1, M=16, O=16)
T = 1 / MMCM2.fout

'''error_values = extract_ila_data(ila_path, 'iladata_falling.csv', index=5, frmt='int')
data_list = get_data_tuple(error_values, T, len(error_values), MMCM1, MMCM2, mode='incremental')
x_values = [data[0] for data in data_list]
y_values = [data[1] for data in data_list]
max_y = max(y_values)
y_values = [value/max_y for value in y_values]

error_values = extract_ila_data(ila_path, 'iladata_rising.csv', index=5, frmt='int')
data_list = get_data_tuple(error_values, T, len(error_values), MMCM1, MMCM2, mode='incremental')
x_values2 = [data[0] for data in data_list]
y_values2 = [data[1] for data in data_list]
max_y = max(y_values2)
y_values2 = [value/max_y for value in y_values2]

error_values = extract_ila_data(ila_path, 'iladata2.csv', index=5, frmt='int')
data_list = get_data_tuple(error_values, T, len(error_values), MMCM1, MMCM2, mode='incremental')
x_values3 = [data[0] for data in data_list]
y_values3 = [data[1] for data in data_list]
max_y = max(y_values3)
y_values3 = [value/max_y for value in y_values3]
plt.plot(x_values, y_values, x_values2, y_values2, x_values3, y_values3)
plt.show()'''

#error_values = extract_ila_data(ila_path, 'iladata.csv', index=5, frmt='int')
#txt_file = os.path.join(r'C:\Users\t26607bb\Desktop', 'Tx.txt')
txt_file = os.path.join(r'/home/bardia/Desktop', 'Tx.txt')
chars = pack_data(txt_file, 2)
error_values = convert_data(chars)
data_list = get_data_tuple(error_values, T/2, len(error_values), MMCM1, MMCM2, mode='incremental')
x_values = [data[0] for data in data_list]
y_values = [data[1] for data in data_list]
max_y = max(y_values)
y_values = [value/max_y for value in y_values]
plt.plot(x_values, y_values)
plt.axhline(y = 0.5, color = 'r', linestyle = '--')
plt.show()

print('--- %s seconds ---' %(time.time() - start_time))