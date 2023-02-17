from sampling import *
from matplotlib import pyplot as plt
import time

# x = []
# for _ in range(1000):
#     x.append(geometric_exp(Fraction(1,10)))

# plt.hist(x, bins=100)
# plt.show()

start = time.time()
for _ in range(1000):
    z = geometric_exp(Fraction(100,1))
end = time.time()
print('fast takes {}'.format(end-start))

start = time.time()
for _ in range(1000):
    z = geometric_exp1(Fraction(100,1))
end = time.time()
print('slow takes {}'.format(end-start))