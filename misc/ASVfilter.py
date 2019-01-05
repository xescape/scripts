'''
Created on Jun 4, 2018

@author: Javi
'''
import re 

def filter_tsv(data, n):
    '''
    filters an abundance file for the top n, returns as a list of lines
    also returns the id of the ASVs retained for the fsa filter
    '''
    
    def abu_sum(line):
        split = re.split('\t', line)
        vals = [float(x) for x in split[1:]]
        return sum(vals)
    
    def getname(line):
        split = re.split('\t',line)
        return split[0]
    
    lines = re.split('\n', data)[:-1] #there'll be an empty line in the end
    
    header = lines[:2]
    rest = sorted(lines[2:], key=abu_sum, reverse=True)[:n]
    names = [getname(x) for x in rest]
    
    return header + rest, names
        
        
def filter_fsa(data, names):
    '''
    takes a fasta, removes any names that don't appear in names
    return as a list of lines
    '''
    
    def check_name(entry):
        name = re.search('>(.+?)\n', entry).group(1)
        return name in names
        
    seqs = re.split('\n(?=>)', data)
    
    return filter(check_name, seqs)
    
    
    

if __name__ == '__main__':
    directory = 'D:/cbw'
    prefix = '16S'
    
    fsa = '/'.join([directory, prefix]) + ".fasta"
    abu = '/'.join([directory, prefix]) + ".tsv"
    
    fsa_outpath = '/'.join([directory, prefix]) + "_filtered.fasta"
    abu_outpath = '/'.join([directory, prefix]) + "_filtered.tsv"
    
    with open(abu, 'r') as input:
        tsv_out, names = filter_tsv(input.read(), 100)
    
    with open(abu_outpath, 'w') as output:
        output.write('\n'.join(tsv_out))
    
    with open(fsa, 'r') as input:
        fsa_out = filter_fsa(input.read(), names)
    
    with open(fsa_outpath, 'w') as output:
        output.write('\n'.join(fsa_out))
    
    print('done!')