import numpy as np
from numpy import linalg as LA

A = np.array([[1, 0, 1, 0, 0, 0], 
              [0, 1, 0, 0, 0, 0], 
              [1, 1, 0, 0, 0, 0], 
              [1, 0, 0, 1, 1, 0], 
              [0, 0, 0, 1, 0, 1]])
print (A)
T, S, D = LA.svd(A,full_matrices=False)

assert np.allclose(A, np.dot(T, np.dot(np.diag(s), Vh)))
