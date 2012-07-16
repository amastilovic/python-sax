import unittest
import numpy as np
import random
import math

from nose import with_setup
from pysax import SAX

__author__ = "Aleksandar Mastilovic"
__copyright__ = "Copyright 2012, Aleksandar Mastilovic"
__credits__ = ["Aleksandar Mastilovic"]
__version__ = "1.0.1"
__maintainer__ = "Aleksandar Mastilovic"
__email__ = "aleksandar.mastilovic@gmail.com"
__status__ = "Development"


class test(unittest.TestCase):

    def setUp(self):
        self.sax = SAX()
        self.delta = 1.0e-10

    def testEuclideanDistance(self):
        sig1 = [ i for i in xrange(100) ]
        sig2 = [ i + 0.5 for i in xrange(100) ]
        lse = self.sax.euclidean_dist(sig1, sig2)
        assert lse == 5.0

    def testNormalizeOnRandom(self):
        orig_sig = [ random.uniform(0, 1) for x in xrange(1000) ]
        sig = self.sax.normalize(orig_sig)

        # properly Z-normalized signal should have a mean
        # very close to 0 and standard deviation very close to 1.0
        assert abs(np.mean(sig)) < self.delta
        assert abs(np.std(sig) - 1.0) < self.delta

    def testPAA(self):
        siglen = 100
        M = 10
        orig_sig = [ random.uniform(0, 1) for x in xrange(siglen) ]
        paa_sig = self.sax.to_PAA(orig_sig, M)

        assert len(paa_sig) == M
        assert np.mean(self.sax.normalize(orig_sig[:M])) == paa_sig[0]

    def testPAAexample(self):
        orig_sig = [2.02, 2.33, 2.99, 6.85, 9.20, 8.80, 7.50, 6.00, 5.85, 3.85, 4.85, 3.85, 2.22, 1.45, 1.34]
        M = 9
        paa_sig = self.sax.to_PAA(orig_sig, M)
        res_sig = [-0.9327168, -0.3699053, 1.383673, 1.391248, 0.6299752, 0.01641218, -0.05933634, -0.8387886, -1.220561]

        assert len(paa_sig) == len(res_sig)

        M = 5
        paa_sig = self.sax.to_PAA(orig_sig, M)
        res_sig2 = [-0.9379922, -0.0857173, 0.4738943, 1.444949, -0.8951336]

        assert len(paa_sig) == len(res_sig2)
