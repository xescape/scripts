'''
Created on Feb 16, 2018

@author: javi
'''
import subprocess
import os
import re

if __name__ == '__main__':
    
    flash_path = "/home/javi/ProgramFiles/FLASH-1.2.11/flash"
    directory = "/data/new/javi/neis/ngo4/N20" #change as needed
    format = "^(.+)[_]R[12].fastq"
    outpath = directory + "/merged"
    
    if not os.path.isdir(outpath): os.mkdir(outpath)
    
    names = set([re.match(format, x).groups(1)[0] for x in os.listdir(directory) if re.match(format, x)])
    
    print(names)
    
    os.chdir(directory)
    
    for name in names:
        with open("./merged/" + name + ".fastq", 'w') as f:
            args = [flash_path, name + "_R1.fastq", name + "_R2.fastq", "-c"]
            subprocess.call(args, stdout = f)
    
    print("done.")
    