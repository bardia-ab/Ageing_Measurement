from resources.clock_manager import CM
import os, re, math, shutil, pickle, bz2

def pack_bytes(data, N_bytes):
    packets = []
    for i in range(0, len(data), N_bytes):
        packet = ''
        for j in range(N_bytes):
            packet += format(data[i + j], '02x')

        packets.append(packet)

    return packets

def pack_data(path, num_bytes):
    # It takes a text file path and groups the received data according to num_bytes determined in the HDL
    file = open(path)
    lines = file.readlines()
    file.close()

    chars = []
    n = num_bytes * 2
    for line in lines:
        if line.endswith('454E44'):
            line = line[:-6]
        else:
            pass
            #breakpoint()

        if len(lines) != 1:
            chars.extend(line.split())
        else:
            for i in range(0, len(line), n):
                chars.extend([lines[0][i:i + n]])

    return chars

def convert_data(chars):
    # It converts hex values into decimal values
    Tx = []
    for char in chars:
        Tx.append(int(char, 16))

    return Tx

def extract_ila_data(load_path, FileName1, index, frmt):
    # index is the number of the desired column starting from 0
    # frmt: 1- int    2- hex
    values = []
    with open(os.path.join(load_path, FileName1)) as file:
        lines = file.readlines()

    for line in lines:
        if not re.match('^\d', line):
            continue

        line = line.rstrip('\n').split(',')
        if frmt == 'hex':
            values.append(int(line[index], base=16))
        else:
            values.append(int(line[index]))

    return values

def get_data_tuple(values, T, N, *CMs: CM, mode='set'):
    # mode: 1-set 2-incremental
    # in mode = set the order of CMs is important CM1, CM2
    # T is the clock period in seconds
    # N is the number of samples
    samples = []
    if mode == 'incremental':
        sps = 0
        for cm in CMs:
            if cm.mode == 'incremental':
                sps += cm.sps
            else:
                sps -= cm.sps

        for i in range(N):
            sample = (T - i * sps) % (T + 0.1)  # % T + 0.1: to limit sample values between 0 and T
            samples.append(sample)
    else:
        num_set_samples = int(56 * CMs[1].O)
        num_sets = int(CMs[0].fvco / abs(CMs[0].fvco - CMs[1].fvco))

        for N1 in range(num_sets):
            for N2 in range(num_set_samples):
                sample = (T - N1 * CMs[0].sps - N2 * CMs[1].sps) % (T + 0.1)
                samples.append(sample)

    data_tuple = list(zip(samples, values))
    data_tuple = sorted(data_tuple, key= lambda x: x[0])

    return data_tuple

def decompose_shift_capture(packets, w_shift, w_capture):
    shift_values = []
    CUT_indexes = []
    N_Bytes = math.ceil((w_shift + w_capture) / 8)
    bin_format = f'0{N_Bytes * 8}b'
    for packet in packets:
        bin_value = format(int(packet, base=16), bin_format)
        shift_values.append(int(bin_value[:-w_capture], base=2))
        CUT_indexes.append(bin_value[-w_capture:][::-1])

    return shift_values, CUT_indexes

def extract_delays(shift_values, CUT_indexes, N_Parallel, sps):
    segments = []
    while shift_values:
        segments.append([])
        while 1:
            shift_value = shift_values.pop(0)
            for CUT_idx, val in enumerate(CUT_indexes.pop(0)):
                if val == '1':
                    delay = shift_value * sps
                    segments[-1].append((CUT_idx, delay))

            if len(segments[-1]) >= N_Parallel:
                segments[-1].sort()
                break

            if not shift_values:
                segments[-1].sort()
                break

            '''prev_shift_value = shift_value
            if shift_values:
                if shift_values[0] > prev_shift_value:
                    segments[-1].sort()
                    break
            else:
                segments[-1].sort()
                break'''

    return segments


def create_folder(FolderPath):
    try:
        os.mkdir(FolderPath)
    except FileExistsError:
        shutil.rmtree(FolderPath)
        os.mkdir(FolderPath)

def store_data(Path, FileName, data, SubFolder=False, FolderName=None, compress=True):
    if SubFolder:
        folder_path = os.path.join(Path, FolderName)
        try:
            os.mkdir(folder_path)
        except FileExistsError:
            shutil.rmtree(folder_path)
            os.mkdir(folder_path)

        data_path = os.path.join(folder_path, FileName)
    else:
        data_path = os.path.join(Path, FileName)

    if compress:
        ofile = bz2.BZ2File(data_path, 'wb')
        pickle.dump(data, ofile)
        ofile.close()
    else:
        with open(data_path, 'wb') as file:
            pickle.dump(data, file)

def load_data(Path, FileName, compress=True):
    data_path = os.path.join(Path, FileName)
    if compress:
        ifile = bz2.BZ2File(data_path, 'rb')
        data = pickle.load(ifile)
        ifile.close()
    else:
        with open(data_path, 'rb') as file:
            data = pickle.load(file)

    return data

def validate_result(segments, srcs_path, TC_idx, N_Parallel):
    stats_path = os.path.join(srcs_path, f'{TC_idx}')
    with open(os.path.join(stats_path, 'stats.txt')) as lines:
        N_segments = int(re.search('\d+', next(lines))[0])
        N_partial = int(re.search('\d+', next(lines))[0])

    if N_partial > 0:
        l_segments = N_segments + 1
        if all(map(lambda x: len(x) == N_Parallel, segments[:-1])) and len(segments[-1]) == N_partial and len(segments) == l_segments:
            result = True
        else:
            result = False
    else:
        l_segments = N_segments
        if all(map(lambda x: len(x) == N_Parallel, segments)) and len(segments) == l_segments:
            result = True
        else:
            result = False

    return result
