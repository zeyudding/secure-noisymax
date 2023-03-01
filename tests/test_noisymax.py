from noisymax.primitive import *
from noisymax.algorithm import noisy_top_k, noisy_top_k_secure, noisy_top_k_secure_fast
from matplotlib import pyplot as plt
import time
from fractions import Fraction


def test_noisy_top_k():
    k = 5
    eps = 1
    n = 10
    # q = np.random.randint(low=0, high=100, size=n)
    # q = np.zeros(n)
    q = np.arange(start=0, stop=n, step=1)
    ind, gap = noisy_top_k(q, k, eps)
    # print(ind)
    # print(gap)
    return 0

def test_noisy_top_k_secure():
    k = 5
    eps = Fraction(1,1)
    n = 10
    # q = np.random.randint(low=0, high=100, size=n)
    # q = np.zeros(n)
    q = np.arange(start=0, stop=n, step=1)
    ind, gap = noisy_top_k_secure(q, k, eps, m=10, target_res=Fraction(1,10))
    # print(ind)
    # print(gap)
    return 0

def test_noisy_top_k_secure_fast():
    k = 5
    eps = Fraction(1,1)
    n = 10
    # q = np.random.randint(low=0, high=100, size=n)
    # q = np.zeros(n)
    q = np.arange(start=0, stop=n, step=1)
    ind, gap = noisy_top_k_secure_fast(q, k, eps, m=10, target_res=Fraction(1,10))
    # print(ind)
    # print(gap)
    return 0    


def time_noisy_top_k():
    k = 5
    eps = Fraction(1, 1)
    n_iterations = 10
    ns = list(range(100, 1000, 100))
    run_time = []
    for n in ns:
        # q = np.random.randint(low=0, high=100, size=n)
        # q = np.zeros(n)
        q = np.arange(start=0, stop=n, step=1)
        start = time.time()
        for t in range(n_iterations):
            ind, gap = noisy_top_k(q, k, eps)
        end = time.time()
        t = (end-start)*1_000_000/n_iterations
        run_time.append(t)
    # print(run_time)
    plt.plot(ns, run_time, label="running time noisy_top_k")
    plt.legend(loc="lower right")
    plt.show()
    return run_time


def time_noisy_top_k_secure():
    k = 5
    eps = Fraction(1, 1)
    n_iterations = 10_0
    ns = list(range(100, 1000, 100))
    run_time = []
    for n in ns:
        # q = np.random.randint(low=0, high=100, size=n)
        # q = np.zeros(n)
        q = np.arange(start=0, stop=n, step=1)
        start = time.time()
        for t in range(n_iterations):
            ind = noisy_top_k_secure(q, k, eps)
        end = time.time()
        t = (end-start)*1_000_000/n_iterations
        run_time.append(t)
    # print(run_time)
    plt.plot(ns, run_time, label="running time noisy_top_k_secure")
    plt.legend(loc="lower right")
    plt.show()
    return run_time

def time_noisy_top_k_secure_fast():
    k = 5
    eps = Fraction(1, 1)
    n_iterations = 10_0
    ns = list(range(100, 1000, 100))
    run_time = []
    for n in ns:
        # q = np.random.randint(low=0, high=100, size=n)
        # q = np.zeros(n)
        q = np.arange(start=0, stop=n, step=1)
        start = time.time()
        for t in range(n_iterations):
            ind = noisy_top_k_secure_fast(q, k, eps)
        end = time.time()
        t = (end-start)*1_000_000/n_iterations
        run_time.append(t)
    # print(run_time)
    plt.plot(ns, run_time, label="running time noisy_top_k_sure_fast")
    plt.legend(loc="lower right")
    plt.show()
    return run_time

def time_exp():
    eps = 1
    k = 3
    b = 2*k/eps
    run_time = []
    n_iterations = range(10000, 100000, 5000)
    for n in n_iterations:
        start = time.time()*1_000_000
        # for i in range(n):
        #     rv = np.random.exponential(b)
        rv = np.random.exponential(scale=b, size=n)
        end = time.time()*1_000_000
        t = (end-start)/n
        run_time.append(t)
    return run_time



def time_geometric_exp():
    eps = Fraction(1,1)
    k = 3
    x = eps/(2*k)
    run_time = []
    n_iterations = range(10000, 100000, 5000)
    for n in n_iterations:
        start = time.time()*1_000_000
        for i in range(n):
            rv = geometric_exp(x)
        end = time.time()*1_000_000
        t = (end-start)/n
        run_time.append(t)
    return run_time

if __name__ == '__main__':
    # q = np.zeros(10)
    # k = 3
    # eps = Fraction(10,1)
    # np.random.seed(0)
    # ind, gap = noisy_top_k_secure_fast(q, k, eps, target_res=Fraction(1,10))
    # print(ind, gap)

    ns = list(range(100, 1000, 100))
    t0 = time_noisy_top_k()
    t1 = time_noisy_top_k_secure()
    t2 = time_noisy_top_k_secure_fast()
    ratio1 = np.divide(t1, t0)
    ratio2 = np.divide(t2, t0)
    plt.plot(ns, ratio1, label="noisy_top_k_secure vs noisy_top_k")
    plt.plot(ns, ratio2, label="noisy_top_k_secure_fast vs noisy_top_k")
    plt.legend(loc="lower right")
    plt.show()

