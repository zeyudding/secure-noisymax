from sampling_primitive import *
from secure_noisymax import noisy_top_k, noisy_top_k_secure, noisy_top_k_secure_fast
from matplotlib import pyplot as plt
import time
from fractions import Fraction


def test_noisy_top_k():
    # np.random.seed(2022)
    # random.seed(2022)
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
    n_iterations = 10_0
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
    # np.random.seed(0)
    # random.seed(0)
    #
    # 
    #
    # t = test_noisy_top_k_secure()
    #
    # test_noisy_top_k_secure_fast()
    #
    ns = range(10000, 100000, 5000)
    t1 = time_exp()
    t2 = time_geometric_exp()
    ratio = np.divide(t2, t1)
    # plt.plot(ns, t1, t2, ratio)
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    ax1.plot(ns, t1, label='numpy.exponential')
    ax1.plot(ns, t2, label='geometric_exp')
    ax1.legend(loc="upper right")

    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111)
    ax2.plot(ns, ratio, label='ratio')
    ax2.legend(loc="upper right")

    plt.show()
    
    # ns = list(range(100, 1000, 100))
    # t0 = time_noisy_top_k()
    # t1 = time_noisy_top_k_secure()
    # t2 = time_noisy_top_k_secure_fast()
    # ratio1 = np.divide(t1, t0)
    # ratio2 = np.divide(t2, t0)
    # plt.plot(ns, ratio1, label="noisy_top_k_secure vs noisy_top_k")
    # plt.plot(ns, ratio2, label="noisy_top_k_secure_fast vs noisy_top_k")
    # plt.legend(loc="lower right")
    # plt.show()

    # k = 5
    # eps = Fraction(1,1)
    # ms = range(2, 50, 2)
    # running_time = []
    # n_iterations = 500
    # q = np.arange(n_iterations)
    # for m in ms:
    #     start = time.time()*1_000_000
    #     for i in range(1000):
    #         ind, gap = noisy_top_k_secure_fast(q, k, eps, m)
    #     end = time.time()*1_000_000
    #     running_time.append((end-start)/n_iterations)
    
    # plt.plot(ms, running_time, label="m (precision scaling factor)")
    # plt.legend(loc="lower right")
    # plt.show()