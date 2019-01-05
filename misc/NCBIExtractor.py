'''
Created on Mar 15, 2017

Companion of NCBIDownloader, extracts the fastas generated

@author: javi
'''

if __name__ == '__main__':
    
    from os import chdir, mkdir, scandir
    import re
    from subprocess import check_output
    
    directory = '/data/new/javi/neis/ngo2'
    outpath = '/data/new/javi/neis/ngo_fasta'
    
    chdir(directory)
    
    try:
        mkdir(outpath)
    except Exception:
        print(Exception)
    
    for entry in scandir():
        
        if entry.is_dir():
            
            files = scandir(entry.name)
            name = re.sub(' ', '', entry.name) + '.fasta'
            
            for file in files:
                fn = file.name
                if not (re.search('_cds_', fn) or re.search('_rna_', fn)) and fn.endswith('genomic.fna.gz'):
                    print(fn)
                    fsa = check_output(['gzip', '-cd', '/'.join([entry.name, fn])])
#                     print(' '.join(['gzip', '-cd', '/'.join([entry.name, fn]), '|', 'cat', '>', '/'.join([outpath, name])]))
                    
                    with open('/'.join([outpath, name]), 'w') as output:
                        output.write(fsa.decode("utf-8"))
                    break
    print('Done!')
                    