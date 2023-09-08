import time, pickle, statistics, os, re
import numpy as np
import matplotlib.pyplot as plt
import collections

def pack_data(path, num_bytes):
    # It takes a text file path and groups the received data according to num_bytes determined in the HDL
    file = open(path)
    lines = file.readlines()
    file.close()

    chars = []
    n = num_bytes * 2
    for line in lines:
        if len(lines) != 1:
            chars.extend(line.split())
        else:
            for i in range(0, len(lines[0]), n):
                chars.extend([lines[0][i:i + n]])

    return chars

def convert_ila(load_path, FileName1, store_path):
    file = open(os.path.join(load_path, FileName1))
    lines = file.readlines()
    file.close()

    values = []

    for line in lines:
        if not re.match('^\d', line):
            continue

        line = line.rstrip('\n').split(',')
        value = format(int(line[3]), '04X')
        values.append(value)

    file = open(store_path, 'w+')
    file.writelines(values)
    file.close()

def convert_data(chars):
    # It converts hex values into decimal values
    Tx = []
    for char in chars:
        Tx.append(int(char, 16))

    return Tx

def get_samples(setting, n, offset=0, mode='cascaded', active_CM='1'):
    # mode: 1-'cascaded'    2-'single'
    # active_CM:    '1' & '2'
    # even in 'single' mode, n shows number of repetitive sets
    samples = []
    fin = setting[0]
    D1 = setting[1]
    M1 = setting[2]
    O1 = setting[3]
    D2 = setting[4]
    M2 = setting[5]
    O2 = setting[6]
    Tvco1 = D1 / (M1 * fin)
    Tvco2 = Tvco1 * O1 * D2 / M2
    Tout2 = Tvco2 * O2
    n_s = int(56 * O2)
    s_ps1 = Tvco1 / 56
    s_ps2 = Tvco2 / 56

    if mode == 'cascaded':
        for n1 in range(n):
            first_sample_point = Tout2 - n1 * s_ps1 + offset    # offset = destination_clock - source_clk
            for n2 in range(n_s):
                sample_point = first_sample_point - n2 * s_ps2
                if sample_point > Tout2 or sample_point < Tout2:
                    sample_point = sample_point % Tout2
                samples.append(sample_point)
    if mode == 'single':

        s_ps = s_ps1
        if active_CM == '2':
            s_ps = s_ps2

        for n1 in range(n):
            first_sample_point = Tout2 - n1 * s_ps + offset  # offset = destination_clock - source_clk
            for n2 in range(n_s):
                sample_point = first_sample_point - n2 * s_ps
                if sample_point > Tout2 or sample_point < Tout2:
                    sample_point = sample_point % Tout2
                samples.append(sample_point)

    if mode == 'incremental':
        for k in range(n * n_s):
            sample_point = Tout2 - k * (s_ps1 - s_ps2)
            samples.append(sample_point)

    return samples

def sort_data(samples, Tx, n, desired_settings=None, mode='complete'):    #modes: 1-'partial' 2-'complete'
    # In partial mode specified settings by desire_settings are returned
    # In complete mode all are returned
    n_s = len(Tx) / n
    desired_data_sets = []
    data_pairs = list(zip(samples, Tx))

    if mode == 'partial':
        desired_settings.sort()
        for idx in desired_settings:
            desired_data_sets = desired_data_sets + data_pairs[(idx * n_s):((idx+1) * n_s)]

        desired_data_sets = sorted(data_pairs, key=lambda tup: tup[0])
    else:
        desired_data_sets = sorted(data_pairs, key=lambda tup: tup[0])

    sorted_samples = [tup[0] for tup in desired_data_sets]
    sorted_Tx = [tup[1] for tup in desired_data_sets]

    return sorted_samples, sorted_Tx

def plot(samples, Tx, n, desired_settings=None, scale='on', plot_type='plot'):
    n_desired = len(desired_settings)
    data_sets_list = [[] for _ in range(n_desired)]
    sample_sets_list = [[] for _ in range(n_desired)]
    for idx, data in enumerate(Tx):
        res = idx % n
        set_index = (n - 1) - res
        if set_index not in desired_settings:
            continue
        data_sets_list[desired_settings.index(set_index)].append(data)
        sample_sets_list[desired_settings.index(set_index)].append(samples[idx])

    fig, ax = plt.subplots()
    for idx, setting in enumerate(desired_settings):
        if scale:
            Tx = [data / (2 ** 16 - 1) for data in data_sets_list[idx]]
            samples = [sample * 1e9 for sample in sample_sets_list[idx]]
        else:
            Tx = data_sets_list[idx]
            samples = sample_sets_list[idx]

        if plot_type == 'stem':
            plt.stem(samples, Tx, linefmt='C%d' % (idx % 10), markerfmt='C%do' % (idx % 10), label=setting)
            ax.legend()
        else:
            plt.plot(samples, Tx, '.')

    plt.show()

def get_statistical_results(samples, Tx, n_s, n, num_repeat):
    # It returns the sample list, list of mean values, and list of STD values
    samples_dict = {}
    num_data = n_s * n
    for i in range(num_repeat):
        samples_sorted, Tx_sorted = sort_data(samples, Tx[i * num_data: (i + 1) * num_data], n, desired_settings=None, mode='complete')
        for sample, data in zip(samples_sorted, Tx_sorted):
            if sample not in samples_dict:
                samples_dict[sample] = [data]
            else:
                samples_dict[sample].append(data)

    std_list = []
    mean_list = []
    for sample in samples_dict:
        std = statistics.stdev(samples_dict[sample])
        mean = statistics.mean(samples_dict[sample])
        std_list.append(std)
        mean_list.append(mean)

    return samples_sorted, mean_list, std_list

def plot_statistical(samples, mean_list, std_list):
    ax1 = plt.subplot(211)
    ax1.stem(samples, mean_list)
    plt.title('Mean Value')
    plt.xlabel('Time (ns)')
    plt.ylabel('Error Probability')

    ax2 = plt.subplot(212)
    ax2.stem(samples, std_list)
    plt.title('Standard Deviation')
    plt.xlabel('Time (ns)')
    plt.ylabel('Error Probability ')

    plt.tight_layout()
    plt.show()

