'''
Created on Jan 26, 2018

@author: javi

Find shared regions in between samples in tab network
'''
import re

global targets

def readHeader(line):
    '''reads the header of tab network, returns a sample list'''
    
    split = re.split('\t', line.rstrip())
    
    return split[2:]

def readLine(line):
    '''takes one line, returns a dictionary with {chr, pos, [data]}'''

    split = re.split('\t', line.rstrip())
    chr = split[0]
    pos = split[1]
    data = split[2:]
    
    return {'chr':chr, 'pos':pos, 'data':data}

def isShared(lineobj, inds):
    '''takes a line dictionary, returns t/f'''
    
    data = lineobj['data']
    rel = [data[i] for i in inds] #relevant data
    
    if(len(rel) == 0):
        raise Exception('isShared: no data in line')
        
    
    return len(set(rel)) <= 2 and rel.count(rel[0]) != 2
    
def isSelf(lineobj, ind, color):
    '''like is shared, but looks for self-color'''    
    
    data = lineobj['data']
    rel = data[ind] #relevant data
      
        
    try:
        return rel == color
    except:
        raise Exception('isShared: no data in line')
    
    
if __name__ == '__main__':

#     target = 'BE11-020'
#     color = '#003FFF'
    directory = 'D:/documents/data/neis'
#     filepath = 'tabNetwork.tsv'
#     outpath = 'shared.txt'
#     
#     results = []
#     total = 0
#     
#     with open('/'.join([directory, filepath]), 'r') as f:
#     
#         sampleList = readHeader(f.readline())
#         target_ind = sampleList.index(target)
#         
#         for line in f:
#             parsed = readLine(line)
#             total += 1
#             if(isSelf(parsed, target_ind, color)):
#                 results.append(parsed)
#             
#     print('{0} self out of total of {1}'.format(len(results), total))

# list = green: '#00FF3F' yellow: '#FFBF00' blue: '#003FFF' pink: '#FF00BF'

# for the old one, where you looked for shared stuff between samples
    targets = ['DK12-38', 'BE11-020']
#     directory = '/data/new/javi/neis/results2/cytoscape'
    filepath = 'tabNetwork.tsv'
    outpath = 'shared.txt'
     
    results = []
     
with open('/'.join([directory, filepath]), 'r') as f:
     
    sampleList = readHeader(f.readline())
    target_inds = [sampleList.index(x) for x in targets]
     
    for line in f:
        parsed = readLine(line)
        if(isShared(parsed, target_inds)):
            results.append(parsed)
             
with open('/'.join([directory, outpath]), 'w') as f:
     
    for r in results:
        f.write('\t'.join([r['chr'], r['pos']] + [r['data'][x] for x in target_inds]))
        f.write('\n')