'''
Created on May 16, 2017

@author: javi


Analyzes the content of multi sequence fastas to see what's in there.
'''

import re


def read(path):
    
    with open(path, 'r') as input:
        data = input.read()
    
    pattern = '(?ms)^>(.+?)\n'
    headers = re.findall(pattern, data)

    return headers

def findGenes(headers):
    '''
    finds how many genes are referred to in the file given all the headers
    '''
    
    pattern = '(?s)^.+?\+ (.+?)$'
    genes = set()
    
    for line in headers:
        gene = re.search(pattern, line).group(1)
        if gene not in genes:
            genes.add(gene)
    
    return genes

def findCoreGenes(genes, path):
    
    with open(path, 'r') as input:
        data = input.read()
    
    core_genes = set()
    
    for ind, gene in enumerate(genes):
        print('Core genes: {0} processed out of {1}'.format(ind, len(genes)), end="\r")
        pattern = '(?s){}\n(.+?)\n'
        seqs = re.findall(pattern, data)
        for seq in seqs:
            if re.search('[^-]', seq):
                core_genes.add(gene)
                break
    
    return core_genes

def findAccGenes(path):
    
    with open(path, 'r') as input:
        data = input.read()
        
    blocks = re.split('\>', data)[1:]
    acc_genes = set()
    
    for ind, block in enumerate(blocks):
        print('Acc genes: {0} blocks processed out of {1}'.format(ind, len(blocks)), end="\r")
        pattern = '(?ms).+?[+] (.+?)\n(.+?)\n$'
        match = re.search(pattern, block)
        gene = match.group(1)
        body = match.group(2)
        
        if gene not in acc_genes and not re.search('[^=-]', body):

#             print(body)
#             print(gene)
#             print()
            acc_genes.add(gene)
    print()
    return acc_genes
    
if __name__ == '__main__':
    
    dir = '/data/new/javi/neis/job'
    file = 'BIGSdb_166607_1494887514_31621.xmfa'
#     file = 'cgMLST_aligned.xmfa'
    
    path = '/'.join([dir, file])
    headers = read(path)
    print('finding genes...')
    genes = findGenes(headers)
#     print('finding core genes...')
#     core_genes = findCoreGenes(genes, path)
#     acc_genes = findAccGenes(path)
#     print(len(genes) - len(acc_genes))
#     print(len(acc_genes))
#     core_genes = genes.difference(acc_genes)
    print(len(genes))
#     print(len(list(filter(lambda x: x.startswith('NEIS'), genes))))
#     print(len(core_genes))
    
    
#     from pprint import pprint
#     pprint(sorted(genes))
    