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
    base_url = 'https://pubmlst.org/bigsdb?db=pubmlst_neisseria_isolates&page=downloadSeqbin&isolate_id='
    id_index = 0
    name_index = 1

    
    for entry in info:
        if '/' in entry[name_index]:
            url = base_url + str(entry[id_index])
            name = re.split('/', entry[name_index])[0]
            call(['wget', '-O', '{}.fasta'.format(name), url])
            print(name)

if __name__ == '__main__':
    
    directory = '/data/new/javi/neis'
    table = 'ids.csv'
    out = 'seqs'
    
    chdir('/'.join([directory, out]))
    info = parseCSV('/'.join([directory, table]))
    download(info[1])
    