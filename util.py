# -*- coding: utf-8 -*-

"""
各种工具方法，服务于各处理模块
"""

import config, logging
import csv, os
import soundfile
import random
import numpy as np
from resampy import resample
import numbers


def read_csv(filename):
    '''
    读取简单的csv文件，不带列标题，每行一个列表，元素均为str
    :param filename: csv文件路径
    :return: [['row1 col1', 'row1 col2',...],...]
    '''
    with open(filename) as df:
        datareader = csv.reader(df)
        return list(datareader)


def load_data(data_list_file, dataset_dir):
    '''
    读取csv文件，并加载指定的m个wav文件。csv文件第一列为wav文件名，第二列0/1标记是否故障。
    注意：音频采样率如果与配置不同，会使用重采样方法保证一致。
    :param data_list_file: csv文件路径
    :param dataset_dir: wav文件目录
    :return: audios: m个音频list
            labels: m个 0/1 故障标记
    '''
    data = read_csv(data_list_file)
    audios, labels = [], []
    for d in data:
        audios.append(read_wav(dataset_dir + "/" + d[0]))
        labels.append(int(d[1]))
    return audios, labels


def read_wav(filename):
    '''
    读取wav文件。
    注意：音频采样率如果与配置不同，会使用重采样方法保证一致。
    :param filename: wav文件路径
    :return: audio: 音频信号list
    '''
    audio, samplerate = soundfile.read(filename)
    if samplerate != config.SAMPLE_RATE:
        audio = resample(audio, samplerate, config.SAMPLE_RATE)
        logging.warning("%s samplerate convert from %gHZ to %gHZ" % (filename, samplerate, config.SAMPLE_RATE))
    return audio


def r_abs(X):
    '''
    将所有数值取绝对值
    '''
    if hasattr(X, "__len__"):
        x_list = []
        for e in X:
            x_list.append(r_abs(e))
        return x_list
    else:
        return abs(X)


def mix(signal, noise, snr=0, output=None):
    '''
    将音频信号按指定信噪比混合，如需要同时保存到文件。
    可以传入一段音频信号，或是几段音频信号
    :param signal: [...] 或 [[...]...]
    :param noise: 与signal对应
    :param snr: 信噪比
    :param output: 输出文件名
    :return: 源信号，噪音，混合信号
    '''
    '''
    如果输入list元素为数字，则判断输入一段信号，否则，判断输入多段信号。
    对一段信号，先将源信号与噪音对齐（便之等长），再
    对多段信号，递归调用进行处理。
    '''
    if isinstance(signal[0], numbers.Number):
        # 输入一段信号
        # signal 与 noise 长度可能不等，首先使之等长
        if len(signal) > len(noise):
            start = random.randint(0, len(signal) - len(noise))
            signal = signal[start:(start + len(noise))]
        elif len(signal) < len(noise):
            start = random.randint(0, len(noise) - len(signal))
            noise = noise[start:(start + len(signal))]
        signal = np.array(signal)
        noise = np.array(noise)

        # 根据snr，对噪音信号进行放缩。 snr = 10 log_10( sum(signal**2) / sum(noise**2) )
        # TODO deal with number overflow
        a = np.sqrt(np.sum(signal ** 2) / (np.sum(noise ** 2) * 10 ** (snr / 10)))
        noise = a * noise

        # 混合
        mixture = signal + noise

        # 保存到文件
        if output is not None:
            soundfile.write(output + '.mix.wav', mixture, config.SAMPLE_RATE)
            soundfile.write(output + '.signal.wav', signal, config.SAMPLE_RATE)
            soundfile.write(output + '.noise.wav', noise, config.SAMPLE_RATE)

        return signal, noise, mixture

    # 输入多段信号的情况
    signal_list, noise_list, mix_list = [], [], []
    for i in range(len(signal)):
        if output is None:
            s, n, m = mix(signal[i], noise[i], snr, None)
        else:
            s, n, m = mix(signal[i], noise[i], snr, output[i])
        signal_list.append(s)
        noise_list.append(n)
        mix_list.append(m)
    return signal_list, noise_list, mix_list


def mkdir_p(dir_path):
    '''
    mkdri -p，创建目录，不存在则创建，如需要也创建上级目录
    :param dir_path: 目录路径
    '''
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
