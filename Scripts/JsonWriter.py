'''
Created on Jul 11, 2017

@author: javi
'''

def genData(n):
    import string
    import random
    
    result = {}
    
    nodes = []
    edges = []
    
    colorTable = {}
    color = ['#7fc97f','#beaed4','#fdc086','#ffff99','#386cb0']
    groups = ['A', 'B', 'C']
    ns = 100
    
    names = sorted([''.join(random.sample(string.ascii_letters, 3)) for x in range(n)])
    
    for i, name in enumerate(names):
        node = {}
        node['name'] = name
        node['group'] = groups[i%3]
        node['id'] = str(i)
        node['ids'] = [random.choice(names) for x in range(ns)]
        node['lengths'] = [random.choice([1,2,4,10,15,20]) for x in range(ns)]
        nodes.append(node)
        colorTable[name] = color[i%3]
    
    n = 0    
    for i, source in enumerate(names):
        for j, target in enumerate(names):
            if j > i:
                edge = {}
                edge['source'] = source
                edge['target'] = target
                edge['width'] = str(random.random() * 20)
                n += 1
                edges.append(edge)
    
    
    return {'names': names, 'nodes': nodes, 'edges': edges, 'colorTable': colorTable}

if __name__ == '__main__':
    
    directory = '/home/javi/workspace/popnetd3-front'
    filename = 'data.json'
    outpath = '/'.join([directory, filename])
    
    data = genData(10)
    
    import json
    
    with open(outpath, 'w') as output:
        json.dump(data, output)