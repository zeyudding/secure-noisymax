from noisymax.primitive import *
from noisymax.algorithm import noisy_top_k, noisy_top_k_secure, noisy_top_k_secure_fast
from matplotlib import pyplot as plt
import time
from fractions import Fraction



if __name__ == '__main__':
    a = np.arange(6)
    print(a)
    ind = [1, 3, 5]
    b = a[ind]
    c = a[:3]
    print(b, c, a)