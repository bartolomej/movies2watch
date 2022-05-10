import numpy as np
import itertools


class NMF:
    """
    Fit a matrix factorization model for a matrix X with missing values.
    such that
        X = W H.T + E
    where
        X is of shape (m, n)    - data matrix
        W is of shape (m, rank) - approximated row space
        H is of shape (n, rank) - approximated column space
        E is of shape (m, n)    - residual (error) matrix

    The rank represents the (expected) number of features (or patterns) in data.
    Lower rank means higher "compression" that a model produces.
    """

    def __init__(self, rank=10, max_iter=100, eta=0.01):
        """
        :param rank: Rank of the matrices of the model.
        :param max_iter: Maximum nuber of SGD iterations.
        :param eta: SGD learning rate.
        """
        self.error = None
        self.H = None
        self.W = None
        self.rank = rank
        self.max_iter = max_iter
        self.curr_iter = 0
        self.execute = True
        self.eta = eta

    def fit(self, X, verbose=False):
        """
        Fit model parameters W, H.
        :param X:
            Non-negative data matrix of shape (m, n)
            Unknown values are assumed to take the value of zero (0).
        :param verbose:
            Print errors per iterations.
        """
        m, n = X.shape

        """
        Randomly initialise W and H matrix for the linear system X = W * H. 
        """
        W = np.random.rand(m, self.rank)
        H = np.random.rand(n, self.rank)

        # Indices to model variables
        w_vars = list(itertools.product(range(m), range(self.rank)))
        h_vars = list(itertools.product(range(n), range(self.rank)))

        # Indices to nonzero rows/columns
        nzcols = dict([(j, X[:, j].nonzero()[0]) for j in range(n)])
        nzrows = dict([(i, X[i, :].nonzero()[0]) for i in range(m)])

        # nzrows[i] <- vrni stolpce j, tako da x_ij > 0

        # Errors
        self.error = np.zeros((self.max_iter,))

        for t in range(self.max_iter):
            if not self.execute:
                self.execute = True
                return

            np.random.shuffle(w_vars)
            np.random.shuffle(h_vars)

            for i, k in w_vars:
                wgrad = sum([(X[i, j] - W[i, :].dot(H[j, :])) * W[i, k] for j in nzrows[i]])
                W[i, k] = max(0, W[i, k] + self.eta * wgrad)

            for j, k in h_vars:
                hgrad = sum([(X[i, j] - W[i, :].dot(H[j, :])) * H[j, k] for i in nzcols[j]])
                H[j, k] = max(0, H[j, k] + self.eta * hgrad)

            self.error[t] = np.linalg.norm((X - W.dot(H.T))[X > 0]) ** 2
            self.curr_iter = t
            if verbose:
                print(t, self.error[t])

        self.W = W
        self.H = H

    def predict(self, i, j):
        """
        Predict score for row i and column j
        :param i: Row index.
        :param j: Column index.
        """
        return self.W[i, :].dot(self.H[j, :])

    def predict_all(self):
        """
        Return approximated matrix for all
        columns and rows.
        """
        return self.W.dot(self.H.T)

    def stop(self):
        self.execute = False
