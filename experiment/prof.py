# import cProfile, pstats, io
from pstats import SortKey
import argparse
import os
import subprocess
import difflib
import logging
import json
import numpy as np
import shutil
import re
import time
from noisymax.primitive import geometric_exp


logger = logging.getLogger(__name__)

def process_datasets(folder):
    logger.info('Loading datasets')
    dataset_folder = os.path.abspath(folder)
    split = re.compile(r'[;,\s]\s*')
    prng = np.random.default_rng()
    default_prng = np.random.default_rng(0)

    for filename in os.listdir(dataset_folder):
        item_sets, records = [], 0
        if filename.endswith('.dat'):
            with open(os.path.join(dataset_folder, filename), 'r') as in_f:
                for line in in_f.readlines():
                    line = line.strip(' ,\n\r')
                    records += 1
                    for ch in split.split(line):
                        item_sets.append(ch)
            item_sets = np.unique(np.asarray(item_sets, dtype=np.int64), return_counts=True)
            logger.info(f'Statistics for {filename}: # of records: {records} and # of Items: {len(item_sets[0])}')
            res = item_sets[1]
            default_prng.shuffle(res)
            yield os.path.splitext(filename)[0], res

def prof_noisy_top_k_secure_fast(q, k, eps_numerator, eps_denominator, m=10, res_numerator=1, res_denominator=10):
    '''
    For timing the noisy_top_k_secure_fast algorithm
    '''
    q_len = len(q)
    # x = eps*target_res/(2*k)
    # res = target_res
    x_numerator = eps_numerator * res_numerator 
    x_denominator = eps_denominator * res_denominator * 2 * k
    res = res_numerator/res_denominator
    curr_res = res

    start = time.time()
    noise = np.array([geometric_exp(x_numerator, x_denominator) for i in range(q_len)])
    noisy_q = q + noise * curr_res
    orig_ind = np.arange(q_len)
    ind = np.argsort(noisy_q)[::-1]
    sorted_noisy_q = noisy_q[ind]
    sorted_orig_ind = orig_ind[ind]
    # print("before loop: noisy_q={}, sorted_q={}, sorted_ind={}".format(noisy_q, sorted_noisy_q, sorted_orig_ind))
    end = time.time()
    t1 = end - start
    
    start = time.time()
    tie = False
    for i in range(k+1):
        if sorted_noisy_q[i] == sorted_noisy_q[i+1]:
            tie = True
            break

    # loop to break ties
    while(tie):
        tie = False
        curr_res /= m
        x_denominator *= m
        # eliminate queries that are not among top k+2
        q_len = len(sorted_noisy_q)
        if q_len > k + 2:
            for i in range(k + 1, q_len - 1):
                if sorted_noisy_q[i] > sorted_noisy_q[i+1]:
                    # ind = ind[:i+1]
                    sorted_orig_ind = sorted_orig_ind[:i+1]
                    sorted_noisy_q = sorted_noisy_q[:i+1]
                    break
        # print("in loop 1: sorted_q={}, sorted_ind={}".format(sorted_noisy_q, sorted_orig_ind))
        noise = np.array([geometric_exp(x_numerator, x_denominator) for i in range(len(sorted_noisy_q))])
        sorted_noisy_q = sorted_noisy_q + (noise % m) * curr_res
        # print("Loop: t = {}, noisy_q = {}".format(t,noisy_q))
        ind = np.argsort(sorted_noisy_q)[::-1]
        sorted_orig_ind = sorted_orig_ind[ind]
        sorted_noisy_q = sorted_noisy_q[ind]
        # print("in loop 2: noise={}, sorted_q={}, sorted_ind={}".format(noise, sorted_noisy_q, sorted_orig_ind))

        # check for ties again
        for i in range(k+1):
            if sorted_noisy_q[i] == sorted_noisy_q[i+1]:
                tie = True
                break
    end = time.time()
    t2 = end-start

    start = time.time()
    # compute gaps
    y = np.random.permutation(k+1)
    gap = []
    for i in range(k):
        if y[i] < y[i+1]:
            gap.append(np.floor((sorted_noisy_q[i]-sorted_noisy_q[i+1]-curr_res)/res)*res)
        else:
            gap.append(np.floor((sorted_noisy_q[i]-sorted_noisy_q[i+1])/res)*res)
    end = time.time()
    t3 = end - start

    #return sorted_orig_ind[:k], gap
    return t1, t2, t3



def main():
    algorithms = (
        prof_noisy_top_k_secure_fast,
    )
    arg_parser = argparse.ArgumentParser(description=__doc__)
    # arg_parser.add_argument('algorithm', help=f'The algorithm to evaluate, options are {algorithms}.')
    arg_parser.add_argument('-n', '--n_iterations', help='The total iterations to run the experiments',
                            required=False, default=1000)
    arg_parser.add_argument('--datasets', help='The datasets folder', required=False)
    arg_parser.add_argument('--output', help='The output folder', required=False,
                            default=os.path.join(os.curdir, 'output'))
    arg_parser.add_argument('--clear', help='Clear the output folder', required=False, default=False,
                            action='store_true')
    
    results = arg_parser.parse_args()
    # default value for datasets path
    results.datasets = os.path.join(os.path.curdir, 'datasets') if results.datasets is None else results
    # chosen_algorithms = algorithm[1:] if chosen_algorithms == 'All' else (chosen_algorithms,)
    output_folder = os.path.abspath(results.output)
    data_folder = os.path.join(output_folder, 'prof')
    if results.clear:
        logger.info('Clear flag set, removing the algorithm output folder...')
        shutil.rmtree(data_folder, ignore_errors=True)
    os.makedirs(data_folder, exist_ok=True)

    
    for dataset in process_datasets(results.datasets):
        dataset_name, dataset_queries = dataset
        json_file = os.path.join(data_folder, f'{dataset_name}.prof.json')
        if os.path.exists(json_file):
            logger.info('Found stored json file, loading...')
            with open(json_file, 'r') as fp:
                data = json.load(fp)
        else:
            logger.info('No json file exists, running experiments...')
            print(dataset_name)
                # print(dataset_queries)
            ks = [25, 50, 100, 200, 400, 800]
            eps_numerator, eps_denominator = 1, 1
            num_iter = 100
            data= {}
            for k in ks:
                prof_time = np.zeros(3)
                for _ in range(num_iter):
                    t1, t2, t3 = prof_noisy_top_k_secure_fast(dataset_queries, k, eps_numerator, eps_denominator)
                    prof_time += [t1, t2, t3]
                # data.append([s1.getvalue(), s2.getvalue(), s3.getvalue()])
                prof_time /= num_iter
                data[k] = prof_time.tolist()
            logger.info('Dumping data into json file...')
            with open(json_file, 'w') as fp:
                json.dump(data, fp)  

if __name__=='__main__':
    main()
