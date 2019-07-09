'''
Created on May 19, 2017

@author: javi
'''
import math
import logging

def main():
    a = range(1000)
    c = 0
    for i in a:
        c += 1
    
    d = [i + 1 for i in a]

    return


if __name__ == '__main__':
    import cProfile
    cProfile.run(main())