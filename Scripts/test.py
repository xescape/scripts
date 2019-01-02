'''
Created on May 19, 2017

@author: javi
'''
import math
def z(x, y, k, m):
#     return (pow(x, 2) + k * pow(y, 2)) / (x + k * y) + m * abs(x - y) / (x + y)
    return x - (x - y) * (1 - x / (x + k * y) - m * (x - y) / (x + y))

if __name__ == '__main__':
    print(z(1000, 5000, 0.6, 0))
    print(z(5000, 1000, 0.6, 0))
    print(z(1000, 5000, 0.6, 0.5))
    print(z(5000, 1000, 0.6, 0.5))