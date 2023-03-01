from noisymax.primitive import *
from noisymax.algorithm import noisy_top_k, noisy_top_k_secure, noisy_top_k_secure_fast
from matplotlib import pyplot as plt
import time

# x = []
# for _ in range(1000):
#     x.append(geometric_exp(Fraction(1,10)))

# plt.hist(x, bins=100)
# plt.show()

input_query = np.arange(0, 1000, 0.1)
num_iter = 10
# print(input_query)
k = 100
eps = 1

start = time.time()
for _ in range(num_iter):
    ind, gap =  noisy_top_k(input_query, k, eps)
end = time.time()
print(f'Noisy top-k with gap: {end-start}')

start = time.time()
for _ in range(num_iter):
    ind, gap =  noisy_top_k_secure(input_query, k, eps)
end = time.time()
print(f'Noisy top-k with gap secure: {end-start}')

start = time.time()
for _ in range(num_iter):
    ind, gap =  noisy_top_k_secure_fast(input_query, k, eps)
end = time.time()
print(f'Noisy top-k with gap secure fast: {end-start}')