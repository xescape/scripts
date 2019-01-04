'''
Created on Jan. 3, 2019

@author: Javi
'''
import re
import pandas

def read(path):
    
    line_template = '(?<!Burkina)(?<!Cambodia)(?<!,)\s(?!$)'  
    df = pandas.read_csv(path, sep=line_template, names=['num', 'accession', 'origin', 'code'], skiprows = 1)
    
    print(df.iloc[3])
    
    
    #take off end whitespace and fix columns
    df['code'] = df['code'].map(lambda x: str(x).strip())
    return df

    
if __name__ == '__main__':
    
    path = '/d/data/plasmo/additional_data/raw_accs.txt'
    output_path = '/d/data/plasmo/additional_data/sec_accs.txt'
    
    df = read(path)
    df.to_csv(output_path, sep='\t', index=False)