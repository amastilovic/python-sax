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


class SAX(object):

    def __init__(self):
        self.prev = 0

    def direction(self):
        v = random.randint(0, 1)
        if v == 0:
            return -1
        return 1

    def random_walk(self, n=1000, maxstep=20):
        def get_rnd():
            self.prev = self.prev + self.direction() * random.uniform(0, maxstep)
            return self.prev
        return [ get_rnd() for i in xrange(n) ]

    def normalize(self, xs):
        X = np.asanyarray(xs)
        return (X-X.mean())/X.std()

    def euclidean_dist(self, x1, x2):
        """Euclidean distance of two signals"""
        l_x1, l_x2 = len(x1), len(x2)
        if l_x1 < l_x2:
            x1.extend([0.0 for i in xrange(l_x2-l_x1)])
        elif l_x2 < l_x1:
            x2.extend([0.0 for i in xrange(l_x1-l_x2)])

        return math.sqrt(sum( math.pow(i-j, 2) for i, j in zip(x1, x2) ))

    def to_PAA(self, vals, M):
        n = len(vals)
        step_f = float(n) / M
        step = int(math.ceil(step_f))
        res = []
        loop = 0
        ptr = int(loop * step_f)
        while ptr <= n-step:
            subarr = np.array( vals[ptr:int(ptr+step)] )
            res.append(np.mean(subarr))
            old_ptr = ptr
            loop += 1
            ptr = int(loop * step_f)

        return np.array(res)

    def convert(self, vals, alphabet):
        paa = self.to_PAA(self.normalize(vals), 8)
        print paa
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
        for v in paa:
            retval.append( map_to_char(v) )

        return retval

if __name__ == "__main__":
    sax = SAX()
    r = sax.random_walk()
    print "+-------------------------------------------------+"
    alphabet = [ 'A', 'B', 'C', 'D', 'E', 'F' ]
    v = sax.convert(r, alphabet)
    for x in v:
        print x,
