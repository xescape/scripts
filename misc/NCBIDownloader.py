'''
Created on Mar 15, 2017

Downloads some genomes from ncbi using a .csv table file

@author: javi
'''
import re 
from subprocess import call
from os import chdir

def parseCSV(path):
    
    with open(path, 'r') as input:
        data = input.read()
    
    entries = []
    
    for line in re.split('\n', data):
        if line == '': 
            continue
        
        entries.append([re.sub(r'^"|"$', '', s) for s in re.split(',', line)]) #strips quotes
        
    legend = entries.pop(0)
    
    return legend, entries


def download(info):
    #downloads files gives a parsed table of info
    name_index = 1
    url_index = -2
    alt_url_index = -1

    
    for entry in info:
        if not entry[url_index] == '-':
            call(['wget', '-r', '-nH', '--cut-dirs=6', entry[url_index]])
            f_name = re.split('/', entry[url_index])[-1]
        else:
            call(['wget', '-r', '-nH', '--cut-dirs=6', entry[alt_url_index]])
            f_name = re.split('/', entry[alt_url_index])[-1]
        
        call(['mv', f_name, re.sub(' |/', '', entry[name_index])])
    
if __name__ == '__main__':
    
    directory = '/data/new/javi/neis/ngo2'
    table = 'ngo_list2.csv'
    
    chdir(directory)
    info = parseCSV('/'.join([directory, table]))
    download(info[1])
    