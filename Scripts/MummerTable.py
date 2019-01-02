'''
Created on May 8, 2018

@author: Javi
'''
import re
import os
import ChrTranslator as ct
import ChrNameSorter as cns
import sys

def addData(f, sampleName, dataTree, reference, organism):
    
    totalCount = 0
    disregardCount = 0
    type = 'snps'

    try:
        data = f.read()
        noHeader = re.search(fetchRegexPattern(f.name), data).group(1)
    except Exception as e:
        print("header parsing error in %s: %s" % (f.name, str(e)))
        sys.exit()
    
    #Divide the remaining data into lines
    rawLines = re.split("\n", noHeader)
    parsed = []
    #Parsing lines
    for line in rawLines[:-1]:
        totalCount += 1
        temp = organizeLine(line, sampleName, type, organism)
        
        #modified for euks!
        if temp is not None and re.search('CHR', temp[0]):
            parsed.append(temp)
        elif temp is None:
            disregardCount += 1
      
#Add the parsed data to the dataTree      
    for dataPoint in parsed:
         
        #Ensures that the branch this data line refers exists.
        #If not, create it 
        currentLevel = dataTree
        for branchName in dataPoint[:2]:
            if branchName not in currentLevel:
                currentLevel[branchName] = {}
            currentLevel = currentLevel[branchName]
        #Adds the SNP value to the tree
        currentLevel[dataPoint[-3]] = dataPoint[-2]
        if reference not in currentLevel:
            currentLevel[reference] = dataPoint[-1]
    
    print("{0!s} disregarded out of {1!s} total".format(disregardCount, totalCount))
    
    return dataTree

def fetchRegexPattern(name):
    print("fetching RegEx for %s" % name)
    if name.endswith(".snps"):
        return "(?s)^.*?=\n(.*)"
    else:
        return "(?sm)^([^#].*)"
    
    
def organizeLine(rawLine, name, type, organism):
    
    lineSplit = re.split("\s+",rawLine)
    try:
        if type is 'snps':
            chr = ct.translate(lineSplit[14].upper(), mode=organism)#for plasmo aligned from 3D7
            ref = lineSplit[2].upper()
            snp = lineSplit[3].upper()
            indel = len(ref) > 1 or len(snp) > 1 or re.search('[^AGCT]', ref) or re.search('[^AGCT]', snp)
            pos = int(lineSplit[1])
            if not indel:
                return [chr, pos, name, snp, ref]
            else:
                return None
        else:
            chr = ct.translate(lineSplit[0].upper(), mode=organism).upper()
            indel = len(lineSplit[3]) > 1 or len(lineSplit[4]) > 1 or re.search('[^AGCT]', lineSplit[3]) or re.search('[^AGCT]', lineSplit[4])
            hetero = re.search("1/1", lineSplit[9])
            quality = float(lineSplit[5])
            pos = int(lineSplit[1])
            snp = lineSplit[4].upper()
            ref = lineSplit[3].upper()
            #choice of 5 as a quality min is a bit arbitrary
            if hetero and not indel and quality > 0:
                return [chr, pos, name, snp, ref] 
            else:
                return None
    except Exception as e:
        print("Illegal Line in file %s: %s" % (name, e))
        print(lineSplit)

def output(f, dataTree, sampleList, organism, reference):
    
    sampleList = sorted(sampleList)
    
    with open(f, 'w') as output:
        header = '\t'.join(['#CHROM', 'POS'] + sampleList) + '\n'
        output.write(header)
        
        for chr in sorted(dataTree.keys(), key=lambda x: cns.getValue(x, organism)):
            for pos in dataTree[chr]:
                d = dataTree[chr][pos]
                line = '\t'.join([chr, str(pos)] + [d[x] if x in d else d[reference] for x in sampleList]) + '\n'
                output.write(line)

if __name__ == '__main__':
    path = 'D:/Documents/data/neis/snps5'
    outpath = 'D:/Documents/data/neis/neis5.tsv'
    organism = 'strep'
    reference = 'FA1090'
    sampleList = []
    
    dataTree = {}
    os.chdir(path)
    
    files = [x for x in os.listdir(path) if x.endswith('.snps')]
    for f in files:
        name = f[:-5]
        sampleList.append(name)
        with open(f, 'r') as input:
            dataTree = addData(input, name, dataTree, reference, organism)
    
    output(outpath, dataTree, sampleList, organism, reference)
    print('Mummer Table Completed')
        