'''
Created on Aug 28, 2017

@author: javi

This script looks for loci that match some clustering pattern. for example, you can look for
places where a certain group of samples cluster together. Another ver of this script might exist
somewhere but I've lost it. 

'''
import re 
from tkinter.tix import ROW

def loadTabNetwork(path):
    
    with open(path, 'r') as input:
        data = input.read()
        
    rows = re.split('\n', data)[:-1]
    
    samplelist = re.split('\t', rows[0])[2:]
    
    pos = []
    rowsplit = []
    for row in rows[1:]:
        tmp = re.split('\t', row)
        pos.append(tmp[:2])
        rowsplit.append(tmp[2:])
    
    return samplelist, pos, rowsplit

def patternSearch(pattern, samplelist, data):
    '''pattern here is a 2D list specifying
    which samples are to be clustered together.
    data is the rowsplit'''
    
    def checkrow(row, idxs):
        if isinstance(idxs[0], list):
            if len(idxs) > 1:
                return checkrow(row, idxs[0]) and checkrow(row, idxs[1:])
            else:
                return checkrow(row, idxs[0])
        else:
            return len(set([row[x] for x in idxs])) == 1
        
    result = []
    
    idxs = [[samplelist.index(sample) for sample in row] for row in pattern]
    
    for i, row in enumerate(data):
        if checkrow(row, idxs): result.append(i)
        
    return result
    
    
        

def condense(rows, size = 1):
    #size now refer to the min size that will count, default 0
    
    results = []
    
    size = size - 1
    pre = 0
    cur = 0
    for row in rows:
                
        if pre == 0:
            pre = row
            cur = row 

        elif (row - cur) != 1:
            if (cur - pre) > size:
                results.append((pre, cur))
            pre = row
            cur = row
        
        else: cur = row 
    
    results.append((pre, row))
        
    return results

if __name__ == '__main__':
    
    directory = '/d/data/neis/results7_d3/cytoscape'
    filename = 'tabNetwork.tsv'
    outname = 'loci.txt'
    
    print('starting!')
    
#     pattern = [["3502","ATL_2011_05-13","GCGS011","GCGS012","GCGS018","GCGS062","GCGS084","GCGS100","GCGS128","GCGS144","GCGS167","GCGS173","GCGS174","GCGS176","GCGS192","GCGS193","GCGS197","GCGS198","GCGS201","GCGS202","GCGS203","GCGS204","GCGS207","GCGS209","GCGS211","GCGS213","GCGS215","GCGS217","GCGS224","GCGS226","MU_NG19","MU_NG20","MU_NG3","MU_NG8","NOR_2011_03-06","SK-92-679","USO_BE10-065","USO_DK11-110","USO_G09-060","USO_G09-145","USO_G13-777","USO_GC3828","USO_GC3831","USO_GC3839","USO_GC3861","USO_GC3863","USO_GC3868","USO_GC3877","USO_GC3879","USO_GE12-070","USO_GR10-009","USO_GR13-015","USO_IE11027","USO_IE11068","USO_IE12-018","USO_NL10-083","USO_NL11143","USO_NO10-026","USO_NO2013-031","USO_SI12-018"]]
    
#    pattern = [["32867", "GCGS044", "GCGS116", "GCGS134", "MIA_2011_05-16", "USO_SP09-048", "USO_SP09-062", "ALB_2011_03_03", "GCGS146", "GCGS210", "GCGS212", "GCGS216"]]

    pattern = [['DK09-023', 'PID1', 'PID18', 'PID24-1', 'PID332']]
    
    samplelist, pos, data = loadTabNetwork('/'.join([directory, filename]))
    rows = patternSearch(pattern, samplelist, data)
    
    crows = condense(rows, 2)
    
    print(crows)
    
    with open('/'.join([directory, outname]), 'w') as output:
        for crow in crows:
            pre = pos[crow[0]]
            post = pos[crow[1]]
            output.write('{0}\t{1}\t--\t{2}\t{3}\n'.format(pre[0], pre[1], post[0], post[1]))
    
    print('loci finder finished with {0} results'.format(len(crows))) 
    
    
