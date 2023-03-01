from noisymax.primitive import *
from matplotlib import pyplot as plt
import numpy as np
import time

# x = []
# for _ in range(1000):
#     x.append(geometric_exp(Fraction(1,10)))

# plt.hist(x, bins=100)
# plt.show()

num_iter = 1000
eps = Fraction(1,1)
k = 3
p = eps/(2*k)



start = time.time()
for _ in range(num_iter):
    z = np.random.exponential(p)
end = time.time()
print(f'exp noise takes {end-start}')

start = time.time()
for _ in range(num_iter):
    z = geometric_exp(p)
end = time.time()
print(f'fast takes {end-start}')

start = time.time()
for _ in range(num_iter):
    z = geometric_exp1(p)
end = time.time()
print(f'slow takes {end-start}')