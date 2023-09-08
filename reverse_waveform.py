from resources.clock_manager import CM
from resources.data_process import *
import matplotlib.pyplot as plt
import time, numpy

start_time = time.time()
ila_path = r'C:\Users\t26607bb\Desktop\CPS_Project\Vivado_Projects\CPS_Single\Results\16-07-2023'

MMCM1 = CM(fin=100e6, D=1, M=15, O=15, mode='incremental', fpsclk=100e6)
MMCM2 = CM(fin=MMCM1.fout, D=1, M=16, O=16, mode='decremental', fpsclk=100e6)
MMCM3 = CM(fin=MMCM1.fout, D=1, M=16, O=16)
T = 1 / MMCM2.fout

plt.rcParams.update({
    "xtick.major.size": 5,
    "xtick.major.pad": 7,
    "xtick.labelsize": 10,
    "ytick.major.size": 5,
    "ytick.major.pad": 7,
    "ytick.labelsize": 10,
    "grid.color": "0.5",
    "grid.linestyle": "--",
    "grid.linewidth": 0.5,
    "lines.linewidth": 2,
    "lines.color": "g",
})

error_values = extract_ila_data(ila_path, 'Falling.csv', index=3, frmt='int')
data_list = get_data_tuple(error_values, T, len(error_values), MMCM1, MMCM2, mode='incremental')
x_values = [data[0]/1e-9 for data in data_list]
y_values = [data[1] for data in data_list]
max_y = max(y_values)
y_values = [value/max_y for value in y_values]

error_values = extract_ila_data(ila_path, 'Rising.csv', index=3, frmt='int')
data_list = get_data_tuple(error_values, T, len(error_values), MMCM1, MMCM2, mode='incremental')
x_values2 = [data[0]/1e-9 for data in data_list]
y_values2 = [data[1] for data in data_list]
max_y = max(y_values2)
y_values2 = [value/max_y for value in y_values2]

error_values = extract_ila_data(ila_path, 'Both.csv', index=3, frmt='int')
data_list = get_data_tuple(error_values, T, len(error_values), MMCM1, MMCM2, mode='incremental')
x_values3 = [data[0]/1e-9 for data in data_list]
y_values3 = [data[1] for data in data_list]
max_y = max(y_values3)
y_values3 = [value/max_y for value in y_values3]

l = len(x_values) // 2
fig = plt.figure()
ax = fig.gca()
ax.set_xticks(numpy.arange(0,5, 5e-2))
ax.set_yticks(numpy.arange(0, 1.1, 0.1))

plt.plot(x_values[:l], y_values[:l], label='Falling', color='#EC407A')
plt.plot(x_values2[:l], y_values2[:l], label='Rising', color='#0097A7')
#plt.plot(x_values3[:l], y_values3[:l], label='Both')
plt.legend(loc='upper right')
plt.grid(True, which='major')
plt.grid(True, which='minor')
plt.xlim([0, 5e-1])
plt.xlabel('Time (ns)', labelpad=10)
plt.ylabel('Error Probability', labelpad=10)
plt.show()


print('--- %s seconds ---' %(time.time() - start_time))