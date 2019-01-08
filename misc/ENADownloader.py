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
from datetime import datetime as dt


def getAcc(sec_acc):
    '''
    returns the run accession from the secondary accession. if there are multiple we return the last one. Probably the best one?
    '''
    
    print('getting acc for ' + sec_acc)
    template = "https://www.ebi.ac.uk/ena/data/view/{0}&display=xml"
    
    res = requests.get(template.format(sec_acc)).content
    
    root = xml.fromstring(res)
    
    try:
        for child in root.find('SAMPLE').find('SAMPLE_LINKS'):
            if child.find('XREF_LINK').find('DB').text == 'ENA-RUN':
                return child.find('XREF_LINK').find('ID').text.strip().split(',')[-1] #we're going to return only the last accession. Hopefully this works. 
    except AttributeError:
        return None

            
def downloadSample(downloader_path, output_path, acc):
    '''
    process one sample. we're going to assume it's just one acc.
    it's actually impractical to do more than 1.
    '''
    
    print('downloading ' + str(acc))
    
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

    sub.run([downloader_path, '-f', 'fastq', '-d', os.path.join(output_path, acc), acc])
          
    os.rename(getPath(acc, 1), getFinalPath(acc, 1))
    os.rename(getPath(acc, 2), getFinalPath(acc, 2))
    os.rmdir(os.path.join(output_path, acc, acc))
    
    logging.info(acc) #TODO

def downloadSampleStar(params):
    return downloadSample(*params)

def checkForCompletion(log, acc):
    '''
    checks if this acc is in the log. Return true if not there.
    '''
    if re.search(acc, log):
        print(acc + ' already done!')
        return False
    return True

def loadTable(input_path):
    '''
    this function will return a table with the column accs from the original 'accession' column
    the accs is always an ndarray. 
    '''
    
    def accHelper(sec_accs):
        arr = [getAcc(sec_acc.strip()) for sec_acc in sec_accs.split(',')]
        return np.array(arr)
        
    df = pandas.read_csv(input_path, sep='\t')
    df['accs'] = df['accession'].apply(accHelper)
    
    #filter out rows where we have no run accs
    df = df.loc[df['accs'].notnull()]
    return df

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
    
    log_path = os.path.join(output_path, 'log.txt')
    acc_path = os.path.join(output_path, 'accs.pkl')
    
    configLogger(log_path)
    
    if not os.path.isfile(acc_path):
        #if this is not a restart, read tsv and make it a hdf
        acc_df = loadTable(input_path)       
        acc_df.to_pickle(acc_path)
    else:
        acc_df = pandas.read_pickle(acc_path)
    
    print(acc_df)
    #get accs of the ones we need to run, then flatten
    accs = acc_df['accs']
    accs = pandas.Series([item for sublist in list(accs) for item in sublist if item != None])
    
    #from here on accs should be a flat series
    if os.path.isfile(log_path):
        with open(log_path, 'r') as f:
            log = f.read()
       
        msk = accs.apply(lambda x: checkForCompletion(log, x))
        accs = accs.iloc[list(msk)]
    
    pool = mp.Pool()   
    pool.map(downloadSampleStar, [(downloader_path, output_path, x) for x in accs])
    
    
    
    
if __name__ == '__main__':
    
#     downloader_path = '/d/data/plasmo/enaBrowserTools/python3/enaDataGet'
#     input_path = '/d/data/plasmo/additional_data/test_accs.txt'
#     output_path = '/d/data/plasmo/additional_data'

#     downloader_path = '/home/javi/workspace/enaBrowserTools/python3/enaDataGet'
#     input_path = '/home/javi/data/plasmo/test_accs.txt'
#     output_path = '/home/javi/data/plasmo'


    downloader_path = '/home/j/jparkin/xescape/programs/enaBrowserTools/python3/enaDataGet'
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    run(downloader_path, input_path, output_path)
    print('ENADownloader Complete.')
     

#TESTING ONLY    
#     print(getAcc('ERS010446'))