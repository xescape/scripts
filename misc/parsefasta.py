import pandas
import numpy
import re
import multiprocessing as mp
import timeit
import os
import re
import logging
from functools import reduce
from collections import deque

def read(path):

    with open(path, 'r') as input:
        return input.read()

def main(path):
    configLogger()
    logger = logging.getLogger()
    logger.info('start')
    global main_data
    main_data = read(path)
    global main_data_length
    main_data_length = len(main_data)

    size = main_data_length // mp.cpu_count()
    chunks = list(range(0, main_data_length, size))
    chunks[-1] = main_data_length

    logger.info('starting map. we have {0} chunks.'.format(len(chunks)-1))

    with mp.Manager() as manager:
        res_lists = [manager.list() for i in range(1, len((chunks)))]

        with manager.Pool(processes = mp.cpu_count()) as pool:
            pool.starmap(worker, [(l, chunks[i-1], chunks[i], i) for i, l in zip(range(1,len(chunks)), res_lists)])
        logger.info('done map')
        # final = deque()
        # for q in res_lists:
        #     # print(len(q))
        #     final.extend(q)
        # logger.info('{0} reads processed'.format(len(list(final))))
        # print(len(final))
    # print(list(res.items())[-1])


def worker(res_list, upper_bound, lower_bound, i):
    def oneRead(read_tup):
        return read_tup[0], "".join(read_tup[1].rstrip('\n').split('\n'))

    logger = logging.getLogger()
    logger.info('{0} starting chunk {1}'.format(os.getpid(), i))

    header = '>'
    pattern = re.compile('(?s)>(.+?)\n(.+?)(?=\n>|$)')
    section = main_data[upper_bound:lower_bound]
    logger.info('{0} starting'.format(os.getpid()))
    reads = re.findall(pattern, section)

    logger.info('{0} processing'.format(os.getpid()))
    res = [oneRead(read) for read in reads]

    logger.info('{0} lookahead'.format(os.getpid()))
    #do the last one
    if len(res) >= 1:
        lookahead_list = [min(lower_bound + 1000, main_data_length), min(lower_bound + 10000, main_data_length), min(lower_bound + 100000, main_data_length), main_data_length]
        last_pattern = re.compile('(?s)>({0})\n(.+?)(?=\n>)'.format(re.escape(res[-1][0])))


        for l in lookahead_list:
            section = main_data[upper_bound:l]
            last_read = re.search(last_pattern, section)
            if last_read:
                res[-1] = oneRead((last_read.group(1), last_read.group(2)))
                break

        if not last_read:
            final_pattern = re.compile('(?s)>({0})\n(.+?)(?=\n$)'.format(re.escape(res[-1][0])))
            final_read = re.search(final_pattern, main_data[upper_bound:main_data_length])
            try:
                res[-1] = oneRead((final_read.group(1), final_read.group(2)))
            except AttributeError:
                logger.info('ATTRIBUTE ERROR by {0} in chunk {1}'.format(os.getpid(), i))

    logger.info('{0} returning'.format(os.getpid()))
    # d.update(dict(res))
    logger.info('{0} found {1} reads'.format(os.getpid(), len(res)))
    res_list.extend(res)
    logger.info('{0} FINISHING chunk {1}'.format(os.getpid(), i))


def configLogger():
    
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter('%(asctime)s:\n%(message)s\n')
    
    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    sh.setFormatter(formatter)
    logger.addHandler(sh)
    
    return logger

if __name__ == "__main__":
    import cProfile
    import sys

    loc = sys.argv[1]

    if loc == 'local':
        path = '/d/data/sp/test.fasta'
    else:
        path = '/gpfs/fs0/project/j/jparkin/Lab_Databases/ChocoPhlAn/ChocoPhlAn.fasta'
        # path = '/scratch/j/jparkin/xescape/test_big.fasta'
    cProfile.run('main(path)', sort='cumtime')
    # main(path)


        







