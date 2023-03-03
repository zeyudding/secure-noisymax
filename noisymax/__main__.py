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
from fractions import Fraction
from noisymax.algorithm import noisy_top_k, noisy_top_k_secure, noisy_top_k_secure_fast


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



def main():
    algorithm = (
        'noisy_top_k_secure_fast',
    )
    parameters = {
        'noisy_top_k_secure_fast': {
            'algorithm': noisy_top_k_secure_fast,
            'metrics': (),
            'plot_function': {},
            'plot_kwargs': {},
            'threshold': (2, 8)
        }
    }
    arg_parser = argparse.ArgumentParser(description=__doc__)
    arg_parser.add_argument('algorithm', help=f'The algorithm to evaluate, options are {algorithm}.')
    arg_parser.add_argument('-n', '--n_iterations', help='The total iterations to run the experiments',
                            required=False, default=1000)
    arg_parser.add_argument('--datasets', help='The datasets folder', required=False)
    arg_parser.add_argument('--output', help='The output folder', required=False,
                            default=os.path.join(os.curdir, 'output'))
    
    results = arg_parser.parse_args()
    # default value for datasets path
    results.datasets = os.path.join(os.path.curdir, 'datasets') if results.datasets is None else results




    for dataset in process_datasets(results.datasets):
        dateset_name, res = dataset
        print(dateset_name)
        print(res)
        ind, gap = noisy_top_k_secure_fast(res, 10, eps=Fraction(1,1))
        print(ind, gap)
        break

if __name__ == '__main__':
    main()