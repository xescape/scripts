import re



def parse(inpath):
    
    with open(inpath, 'r') as input:
        
        results = {}        
        
        for i, line in enumerate(input):
            try:
                date = re.split('\t', line)[14]
                year = int(re.split('/', date)[0])
                try:
                    results[year] += 1
                except:
                    results[year] = 0
            except:
                if(i==0): pass
                else:
                    print('{0} gave an error!'.format(line))
        
    return results


def output(results, outpath):
    
    with open(outpath, 'w') as output:
        output.write('year\tcount\n')
        for key in sorted(results.keys()):
            output.write('{0}\t{1}\n'.format(key, results[key]))

if __name__ == "__main__":
    directory = '/d/data'
    filename = 'eukaryotes.txt'
    inpath = '/'.join([directory, filename])
    outname = 'euseqnums.tsv'
    outpath = '/'.join([directory, outname])
    
    results = parse(inpath)
    
    output(results, outpath)
    
    print('seqnumcount complete.')