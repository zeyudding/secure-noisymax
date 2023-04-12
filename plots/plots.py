import cProfile, pstats, io
from pstats import SortKey
import argparse
import os
import subprocess
import difflib
import logging
import json
import numpy as np
import matplotlib
import shutil
import re
import coloredlogs
import time
from fractions import Fraction

def main():
    data_folder = os.path.join(os.path.curdir, 'output')
    json_file = os.path.join(data_folder, 'prof/kosarak.cprof.json')
    if os.path.exists(json_file):
        with open(json_file, 'r') as fp:
            data = json.load(fp)
            s1 = float(data['s1'].split()[7])
            s2 = float(data['s2'].split()[4])
            s3 = float(data['s3'].split()[4])
            print(s1, s2, s3)
            print(data['s1'])


if __name__ == '__main__':
    main()
    #
    # t = test_noisy_top_k_secure()
    #
    # test_noisy_top_k_secure_fast()
    #
    # ns = range(10000, 100000, 5000)
    # t1 = time_exp()
    # t2 = time_geometric_exp()
    # ratio = np.divide(t2, t1)
    # # plt.plot(ns, t1, t2, ratio)
    # fig1 = plt.figure()
    # ax1 = fig1.add_subplot(111)
    # ax1.plot(ns, t1, label='numpy.exponential')
    # ax1.plot(ns, t2, label='geometric_exp')
    # ax1.legend(loc="upper right")

    # fig2 = plt.figure()
    # ax2 = fig2.add_subplot(111)
    # ax2.plot(ns, ratio, label='ratio')
    # ax2.legend(loc="upper right")

    # plt.show()
    
    # ns = list(range(100, 1000, 100))
    # t0 = time_noisy_top_k()
    # t1 = time_noisy_top_k_secure()
    # t2 = time_noisy_top_k_secure_fast()
    # ratio1 = np.divide(t1, t0)
    # ratio2 = np.divide(t2, t0)
    # plt.plot(ns, ratio1, label="noisy_top_k_secure vs noisy_top_k")
    # plt.plot(ns, ratio2, label="noisy_top_k_secure_fast vs noisy_top_k")
    # plt.legend(loc="lower right")
    # plt.show()

    # k = 5
    # eps = Fraction(1,1)
    # ms = range(2, 50, 2)
    # running_time = []
    # n_iterations = 500
    # q = np.arange(n_iterations)
    # for m in ms:
    #     start = time.time()*1_000_000
    #     for i in range(1000):
    #         ind, gap = noisy_top_k_secure_fast(q, k, eps, m)
    #     end = time.time()*1_000_000
    #     running_time.append((end-start)/n_iterations)
    
    # plt.plot(ms, running_time, label="m (precision scaling factor)")
    # plt.legend(loc="lower right")
    # plt.show()
