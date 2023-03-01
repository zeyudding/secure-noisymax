import numpy as np
from matplotlib import pyplot as plt


# laprv = np.random.laplace(size=10000)
# plt.hist(laprv, density=True, bins=100, histtype='step')
# plt.show()

exprv = np.random.exponential(size=1000000)
plt.hist(exprv, density=True, bins=200, histtype='step')


def expgap(k, sample_size=1000000):
    '''
    return the gap between the top 2 exponential rvs from k rvs
    '''
    exprv = np.random.exponential(size=(k, sample_size))
    # print(exprv)
    sorted = np.sort(exprv, axis=0)
    # print(sorted)
    gap = sorted[-1]-sorted[-2]
    # print(gap)
    return gap

for k in range(2,21,4):
    gap = expgap(k)
    plt.hist(gap, density=True, bins=200, histtype='step')
plt.show()

