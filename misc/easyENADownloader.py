'''
Created on Jan. 2, 2019
Somehow it seems like our job was easier than expected?

@author: Javi
'''

import sys
import subprocess as sub
from pathlib import Path
from shutil import rmtree
from multiprocessing import Pool
import os
import logging
import re

def worker(downloader_path, output_path, acc):
    '''
    process one sample. we're going to assume it's just one acc.
    it's actually impractical to do more than 1.
    '''
    tmp_path = output_path / str(os.getpid())
    os.mkdir(tmp_path)
    
    # print('downloading ' + str(acc))
    logger = logging.getLogger()
    sub.run([downloader_path, '-f', 'fastq', '-d', tmp_path, acc])

    os.rename(tmp_path / acc, output_path / acc)
    os.removedirs(tmp_path)

    logger.info(acc)



def checkForCompletion(accs, log_path, out_path):
    '''
    checks if this acc is in the log. Return true if not there.
    '''
    with open(log_path) as input:
        log_text = input.read()

    res = []
    for acc in accs:
        if acc not in log_text or not verify(acc, out_path):
            t = out_path / acc
            if t.is_dir(): 
                # i = input("Delete partial directory {0}? Y/N")
                # if i.upper() == 'Y':
                #     rmtree(t)
                print('Partial directory found for {0}, moving.'.format(acc))
                t.rename(str(t)+'.old')
            res.append(acc)
            
    
    return res

def verify(acc, out_path):
    suf_1 = '{0}_1.fastq.gz'
    suf_2 = '{0}_2.fastq.gz'

    p1 = out_path / acc / suf_1.format(acc)
    p2 = out_path / acc / suf_2.format(acc)

    if p1.is_file() and p2.is_file():
        return True
    else:
        return False

def loadTable(input_path):
    '''
    We just have a nice txt file with a column full of SRR- accs
    '''
        
    with open(input_path) as input:
        d = input.read()
    
    return d.rstrip('\n').split('\n')

def configLogger(path):
    
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    fh = logging.FileHandler(path)
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: \n %(message)s \n')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    sh.setLevel(logging.INFO)
    logger.addHandler(sh)


def run(downloader_path, input_path, output_path):
    
    log_path = output_path / 'log.txt'
    configLogger(log_path)
    accs = checkForCompletion(loadTable(input_path), log_path, output_path)
    

    print(accs)
    with Pool(processes=4) as pool:
        pool.starmap(worker, [(downloader_path, output_path, acc) for acc in accs])
    
    logger = logging.getLogger()
    logger.info('completed')
    
    
    
    
if __name__ == '__main__':
    
#     downloader_path = '/d/data/plasmo/enaBrowserTools/python3/enaDataGet'
#     input_path = '/d/data/plasmo/additional_data/test_accs.txt'
#     output_path = '/d/data/plasmo/additional_data'

    downloader_path = Path('/d/data/plasmo/enaBrowserTools/python3/enaDataGet')
    input_path = Path('/d/data/plasmo/new_accs.txt')
    output_path = Path('/home/javi/seq')


    # downloader_path = '/home/j/jparkin/xescape/programs/enaBrowserTools/python3/enaDataGet'
    # input_path = sys.argv[1]
    # output_path = sys.argv[2]
    
    run(downloader_path, input_path, output_path)


    # #verify only
    # log_path = output_path / 'log.txt'
    # accs = loadTable(input_path)
    # incomplete = [x for x in accs if not verify(x, output_path)]
    # print('incomplete stuff: {0}'.format(str(incomplete)))
    print('ENADownloader Complete.')
     