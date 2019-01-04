'''
Created on Jan. 2, 2019

@author: Javi
'''
import requests
import sys
import xml.etree.ElementTree as xml
import multiprocessing as mp
import subprocess as sub
import os.path
import os
import pandas
import numpy as np
import logging
import re

def getAcc(sec_acc):
    
    template = "https://www.ebi.ac.uk/ena/data/view/{0}&display=xml"
    
    res = requests.get(template.format(sec_acc)).content
    
    root = xml.fromstring(res)

    for child in root.find('SAMPLE').find('SAMPLE_LINKS'):
        if child.find('XREF_LINK').find('DB').text == 'ENA-RUN':
            return child.find('XREF_LINK').find('ID').text.split(',')

            
def downloadSample(downloader_path, output_path, accs, log_queue):
    '''
    process one sample, combining the various fastqs if necessary
    '''
    
    def getPath(acc, n):
        '''gets the full path for an accession, for cat purposes.
        n means the first or second file'''
        
        return os.path.join(output_path, acc, acc, "{0}_{1}.fastq.gz".format(acc, str(n)))
    
    def getFinalPath(acc, n):
        '''
        so it turns we had to have the downloader go one level deeper.
        then we want to move the file back up
        '''
        return os.path.join(output_path, acc, "{0}_{1}.fastq.gz".format(acc, str(n)))
    
    for acc in accs:
        sub.run([downloader_path, '-f', 'fastq', '-d', os.path.join(output_path, acc), acc])
    
    #merge and move files
    if len(accs) > 1:
        sub.run('cat {0} > {1}'.format(' '.join([getPath(acc, 1) for acc in accs]), getPath(accs[0], 1)))
        sub.run('cat {0} > {1}'.format(' '.join([getPath(acc, 2) for acc in accs]), getPath(accs[0], 2)))
        for acc in accs[1:]:
            os.remove(getPath(acc, 1))
            os.remove(getPath(acc, 2))
            os.rmdir(os.path.join(output_path, acc, acc))
    
    os.rename(getPath(accs[0], 1), getFinalPath(accs[0], 1))
    os.rename(getPath(accs[0], 2), getFinalPath(accs[0], 2))
    os.rmdir(os.path.join(output_path, accs[0], accs[0]))
    
    log_queue.put(acc) #TODO

def downloadSampleStar(params):
    return downloadSample(*params)

def checkForCompletion(log, acc):
    '''
    checks if this acc is in the log. Return true if not there.
    '''
    if re.search(acc, log):
        return False
    return True

def loadTable(input_path):
    '''
    this function will return a table with the column accs from the original 'accession' column
    the accs is always an ndarray. 
    '''
    
    
    df = pandas.read_csv(input_path, sep='\t')
    
    df['accs'] = df['accession'].apply(lambda x: np.array([getAcc(sec_acc) for sec_acc in x.split(',')]).flatten())
    
    return df

def getLogger(name, path):
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    fh = logging.FileHandler(path)
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: \n %(message)s \n')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    
    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    logger.addHandler(sh)
    
    return logger

def logListener(queue, logger):
    
    while True:
        try:
            record = queue.get()
            if record is None:
                break
            logger.info(record)
        except Exception:
            import sys, traceback
            print('Whoops! Problem:', file=sys.stderr)
            traceback.print_exc(file=sys.stderr)

def logListenerStar(params):
    
    logListener(*params)

def run(downloader_path, input_path, output_path):
    
    log_path = os.path.join(output_path, 'log.txt')
    acc_path = os.path.join(output_path, 'accs.pkl')
    
    logger = getLogger('log', log_path)
    log_queue = mp.Manager().Queue()
    
    if not os.path.isfile(acc_path):
        acc_df = loadTable(input_path)['accs']
        acc_df.to_pickle(acc_path)
    else:
        acc_df = pandas.read_pickle(acc_path)
    
    #get accs of the ones we need to run.
    
    with open(log_path, 'r') as f:
        log = f.read()
    msk = list(acc_df.apply(lambda x: checkForCompletion(log, x[0][0])))

    accs = acc_df.iloc[msk]
    
    pool = mp.Pool(mp.cpu_count())
    
    pool.apply_async(logListenerStar, (log_queue, logger))
    
    pool.map(downloadSampleStar, [(downloader_path, output_path, x, log_queue) for x in accs])
    
    log_queue.put(None)
    
    
    
if __name__ == '__main__':
    
    downloader_path = '/d/data/plasmo/enaBrowserTools/python3/enaDataGet'
    downloader_path = '/home/j/jparkin/xescape/programs/enaBrowserTools/python3/enaDataGet'
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    run(downloader_path, input_path, output_path)
    print('ENADownloader Complete.')
     

#TESTING ONLY    
#     print(getAcc('ERS010446'))