import unittest
import numpy as np
from nmf import NMF


class NmfTestCase(unittest.TestCase):
    def test_nmf_fit(self):
        m = 100  # number of rows
        n = 80  # number of columns
        rank = 5  # model rank
        error = 0.1  # error
        A = np.random.rand(m, rank * 2)
        B = np.random.rand(n, rank * 2)
        X = A.dot(B.T) + error * np.random.rand(m, n)  # generate random dataset
        model = NMF(rank=rank, max_iter=20, eta=0.001)
        model.fit(X, verbose=True)
        model.predict_all()
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
