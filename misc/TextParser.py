'''
Created on May 26, 2017

@author: javi

Parses a text file containing lines of text into a popnet-readable thing

was for the birthday card network
'''

import re

def read(path):
    with open(path, 'r') as input:
        data = input.read()
    
    
    pattern = '@(.+?)\n(.+?)$'
    entries = re.split('\n\n', data)[:-1]
    
    result = {}
    total = set() #all words
    
    for entry in entries:
        match = re.match(pattern, entry)
        name = match.group(1)
        text = match.group(2)
        words = toWords(text)
        result[name] = words
        total.update(words)
    
    return result, total

def toWords(string):
    
    string = re.sub('[^a-zA-Z0-9 ]', '', string)
    words = set(re.split('\s', string))
    return words
    
def makeTable(result, total, path, legpath):
    
    def translate(word, name):
        if word in result[name]: return 'T'
        else: return '-'
    
    strings = []
    legstrings = []
    dist = 10000
    chrname = 'STREP_CHRI'
    
    names = sorted(result.keys())
    strings.append('\t'.join(['', ''] + names))
    
    index = 0
    for word in sorted(total):
        tmp = [translate(word, x) for x in names]
        if tmp.count('T') <= 1: continue
        tmp.insert(0, str(index * dist))
        tmp.insert(0, chrname)
        strings.append('\t'.join(tmp))
        legstrings.append('\t'.join([str(index * dist), word]))
        index += 1
    
    with open(path, 'w') as output:
        output.write('\n'.join(strings))
    
    with open(legpath, 'w') as output:
        output.write('\n'.join(legstrings))

if __name__ == '__main__':
    
    dir = '/home/javi/Desktop/bt'
    file = 'input.txt'
    output = 'output.txt'
    legend = 'legend.txt'
    
    inpath = '/'.join([dir, file])
    outpath = '/'.join([dir, output])
    legpath = '/'.join([dir, legend])
    
    result, total = read(inpath)
    makeTable(result, total, outpath, legpath)