'''
script that checks how much drift there actually is, slowwwly. 
usage: drift_check.py [path_to_input] [path_to_output]
outputs a tsv in the format of:

1 A:10    B:5...
2 A:10   B:3...

'''
def parse(path):

    def splitLine(line):
        return line.rstrip('\t').split('\t')
    with open(path, 'r') as input: 
        data = input.read() 
    
    lines = data.rstrip('\n').split('\n')
    rows = [splitLine(line) for line in lines]
    return rows

def count(row):
    #given one row, return the test statistics. 

    pos = row[1]
    bases = row[2:]

    unique_bases = set(bases)
    counts = [bases.count(base) for base in unique_bases]

    return (pos, sorted(zip(unique_bases, counts), key=lambda x: x[1], reverse=True))

def countSummary(count_results):
    #make a summary. how many are drift.
    drift_count = 0

    for row in count_results:
        pos, counts = row
        l = len(counts)
        if l <= 1:
            drift_count += 1
        elif l >= 3:
            pass
        elif counts[1][1] <= 1:
            drift_count += 1
    
    return '{0} drift position out of {1}, for a total of {2} percent\n'.format(str(drift_count), str(len(count_results)), str(drift_count / len(count_results) * 100)[:6])



def makeOutput(row_data):
    pos, counts = row_data
    return '\t'.join([str(pos)] + ['{0}:{1}'.format(str(base), str(count)) for base, count in counts])

if __name__ == '__main__':
    import sys
    path = sys.argv[1]
    out_path = sys.argv[2]

    rows = parse(path)
    count_results = [count(row) for row in rows]

    with open(out_path, 'w') as output:
        output.write(countSummary(count_results))
        output.write('\n'.join([makeOutput(row) for row in count_results]))

    

