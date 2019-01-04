'''
Created on May 19, 2017

@author: javi
'''
import math
import logging

def getLogger(name, path):
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    fh = logging.FileHandler(path)
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: \n %(message)s \n')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    
    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    logger.addHandler(sh)
    
    return logger

def z(x, y, k, m):
#     return (pow(x, 2) + k * pow(y, 2)) / (x + k * y) + m * abs(x - y) / (x + y)
    return x - (x - y) * (1 - x / (x + k * y) - m * (x - y) / (x + y))

if __name__ == '__main__':
    logger = getLogger('log', '/d/workspace/Personal/Scripts/log.txt')
    logger.info('testmessage')
    logger.info('test2')