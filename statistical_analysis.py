from Samples_Functions import *

start_time = time.time()
################## Main #########################
path = r'P:\Desktop\Tx.txt'
fin1 = 100e6
D1 = 1
M1 = 15
O1 = 15
D2 = 1
M2 = 16
O2 = 16
n = 15  # It shows number of sets
num_repeat = 100

setting = [fin1, D1, M1, O1, D2, M2, O2]
n_s = 56 * O2   # It shows number of sample points in a set

chars = pack_data(path, 2)
Tx = convert_data(chars)
samples = get_samples(setting, n, offset=0) # offset = destination_clock - source_clk
samples_sorted, mean_list, std_list = get_statistical_results(samples, Tx, n_s, n, num_repeat)
#sorted_samples, sorted_Tx = sort_data(samples, Tx[(n_s * n * 99):(n_s * n * 100)], n, desired_settings=[], mode='complete')

plot_statistical(samples_sorted, mean_list, std_list)
#plot(sorted_samples, sorted_Tx, n, desired_settings=range(n), scale='on')

print('--- %s seconds ---' %(time.time() - start_time))