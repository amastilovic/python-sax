#!/usr/bin/env python

import os
import logging

import random
import numpy as np
import math

__author__ = "Aleksandar Mastilovic"
__copyright__ = "Copyright 2012, Aleksandar Mastilovic"
__credits__ = ["Aleksandar Mastilovic"]
__version__ = "1.0.1"
__maintainer__ = "Aleksandar Mastilovic"
__email__ = "aleksandar.mastilovic@gmail.com"
__status__ = "Development"


logger = logging.getLogger('create_bitmap')

def direction():
    v = random.randint(0, 1)
    if v == 0:
        return -1
    return 1

prev = 0

def random_walk(n=1000, maxstep=2):
    def get_rnd():
        global prev
        prev = prev + direction() * random.randint(0, maxstep)
        return prev
    res = [ get_rnd() for i in xrange(n) ]
    return res

def conv_to_PAA(vals, N, n):
    res = []
    for i in range(0, len(vals)-N+1):
        subarr = np.array(vals[i:i+N])
        # normalize
        m = np.mean(subarr)
        s = np.std(subarr)
        subarr = [ (x-m)/s for x in subarr ]
        # convert to PAA
        tmp = [ np.mean(subarr[i:i+N/n]) for i in xrange(0, len(subarr), N/n) ]
        res.append(tmp)
    return np.array(res)

def conv_to_SAX(vals, alphabet):
    paa = conv_to_PAA(vals, 16, 8)
    max_paa = np.max(paa)
    min_paa = np.min(paa)
    alen = len(alphabet)
    step = (max_paa - min_paa) / alen
    def map_to_char(v):
        idx = int(abs(v-min_paa)/step)
        if idx >= alen:
            idx = alen - 1
        return alphabet[idx]

    retval = []
    for row in paa:
        retval.append( [ map_to_char(v) for v in row ] )
    return retval

if __name__ == "__main__":
    r = random_walk()
    print "+-------------------------------------------------+"
    alphabet = [ 'A', 'B', 'C', 'D', 'E', 'F' ]
    v = conv_to_SAX(r, alphabet)
    for x in v:
        print x
    
    
        
