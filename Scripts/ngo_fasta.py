'''
Created on May 24, 2018

makes snps files using nucmer

@author: Javi
'''
import os
import re
from multiprocessing import Pool
import subprocess as sp

def nucmer(file, ref, outpath):
       
    name = findName(file)
    
    if name+'.snps' in os.listdir(outpath):
        print(name+" is already done!")
        return
    
    nuc_command = ['nucmer', '--prefix='+name, ref, file]
    filter_command = ['delta-filter', '-r', '-q', name+'.delta', '>', name+'.filter']
    snps_command = ['show-snps', '-Clr', name+'.filter', '>', outpath+'/'+name+'.snps']
    
    print(name+': starting nucmer')
    nuc_result = sp.run(nuc_command, stderr=sp.STDOUT, stdout=sp.PIPE, encoding='UTF-8')
    print(nuc_result.stdout)
    
    print(name+': starting filter')
    filter_result = sp.run(' '.join(filter_command), shell = True, stderr=sp.STDOUT, stdout=sp.PIPE, encoding='UTF-8')
    print(filter_result.stdout)
    
    print(name+': starting show-snps')
    snps_result = sp.run(' '.join(snps_command), shell = True, stderr=sp.STDOUT, stdout=sp.PIPE, encoding='UTF-8')
    print(snps_result.stdout)

#use if you need to alter the name for formatting. specific to each data set.
def findName(raw):

    pattern = '^PRO1650_(.+?)_'
    pattern2 = '(.+?).fasta'
    try:
        name = re.match(pattern, raw).group(1)
    except:
        name = re.match(pattern2, raw).group(1)
    
    return name
    

if __name__ == '__main__':
    
    directory = '/data/new/javi/neis/ngo4/N20/merged/fasta'
    outpath = 'snps'
    logpath = 'log.txt'
    ref = 'FA1090.fasta' 
    files = [x for x in os.listdir(directory) if x.endswith('fasta')]
    print(files)
    os.chdir(directory)
    
    try:
        os.mkdir(outpath)
    except:
        pass
    
    
        
    
    with Pool(processes=4) as pool:
        pool.starmap(nucmer, [(x, ref, outpath) for x in files])
        