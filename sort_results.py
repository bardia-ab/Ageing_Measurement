from Samples_Functions import *

start_time = time.time()
################## Main #########################
path = r'P:\Desktop\Tx.txt'
#path = r'\\nask.man.ac.uk\home$\Desktop\Tx.txt'
ila_path = r'C:\Users\t26607bb\Desktop\CPS_Project\Vivado_Projects\CPS_Single\Results'
fin1 = 100e6
D1 = 1
M1 = 15
O1 = 15
D2 = 1
M2 = 16
O2 = 16
n = 15  # It shows number of sets

setting = [fin1, D1, M1, O1, D2, M2, O2]
n_s = 56 * O2   # It shows number of sample points in a set

convert_ila(ila_path, 'iladata.csv', path)
chars = pack_data(path, 2)
Tx = convert_data(chars)
samples = get_samples(setting, n, offset=0, mode='incremental') # offset = destination_clock - source_clk
sorted_samples, sorted_Tx = sort_data(samples, Tx, n, desired_settings=[], mode='complete')

plot(sorted_samples, sorted_Tx, n, desired_settings=range(n), scale='on', plot_type='stem') #plot_type: stem or plot

print('--- %s seconds ---' %(time.time() - start_time))