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
    algorithms = (
        noisy_top_k_secure_fast,
        noisy_top_k_secure,
        noisy_top_k
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
    data_folder = os.path.join(output_folder, 'time')
    if results.clear:
        logger.info('Clear flag set, removing the algorithm output folder...')
        shutil.rmtree(data_folder, ignore_errors=True)
    os.makedirs(data_folder, exist_ok=True)

    for algorithm in algorithms:
        json_file = os.path.join(data_folder, f'{algorithm.__name__}.json')
        if os.path.exists(json_file):
            logger.info('Found stored json file, loading...')
            with open(json_file, 'r') as fp:
                data = json.load(fp)
        else:
            logger.info('No json file exists, running experiments...')
            ks = [25, 50, 100, 200]
            eps=Fraction(1,1)
            num_iter = 100
            data = {}
            
            for dataset in process_datasets(results.datasets):
                dataset_name, dataset_queries = dataset
                # data = evaluate(
                #     algorithm=evaluate_algorithm, input_data=dataset, metrics=metrics, epsilons=epsilons,
                #     threshold=threshold, k_array=k_array, counting_queries=results.counting,
                #     total_iterations=int(results.n_iterations)
                # )
                print(dataset_name)
                print(dataset_queries)
                data[dataset_name] = []
                for k in ks:
                    start = time.time()
                    for _ in range(num_iter):
                        ind, gap = algorithm(dataset_queries, k, eps)
                    end = time.time()
                    data[dataset_name].append([k,(end-start)/num_iter])
            
            logger.info('Dumping data into json file...')
            with open(json_file, 'w') as fp:
                json.dump(data, fp)   

if __name__ == '__main__':
    main()