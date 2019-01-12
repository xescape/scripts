'''
Created on Jan. 12, 2019

@author: javi

recursively touches everything that fits some criteria under a folder.
'''
import pathlib

def check(name):
    '''
    checks if a file fits the criteria. modify each time as needed
    '''
    
    return True

def recursiveTouch(path):
    '''path is a directory'''
    
    for x in path.iterdir():
        if x.isdir():
            recursiveTouch(path/x)
        else:
            if check(x):
                x.touch()
            else:
                print('skipping ' + str(x))

if __name__ == '__main__':
    import sys
    dir = sys.argv[1]
    path = pathlib.Path(dir)
    if path.is_dir():
        recursiveTouch(path)
    else:
        raise(FileNotFoundError('this isnt even a directory'))
    
    print('done!')    
    