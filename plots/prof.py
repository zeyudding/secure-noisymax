import cProfile, pstats, io
from pstats import SortKey
from fractions import Fraction
import numpy as np
from noisymax.primitive import geometric_exp

# pr = cProfile.Profile()
# pr.enable()
# # ... do something ...
# pr.disable()
# s = io.StringIO()

def prof_noisy_top_k_secure_fast(q, k, eps, m=10, target_res=Fraction(1, 10)):
    '''
    Similar to noisy_top_k_secure() but with early query elimination 
    '''
    q_len = len(q)
    x = eps*target_res/(2*k)
    res = target_res

    pr1 = cProfile.Profile()
    pr2 = cProfile.Profile()
    pr3 = cProfile.Profile()
    pr1.enable()

    noise = np.array([geometric_exp(x) for i in range(q_len)])
    # noise = np.array([1, 1, 1, 1, 1, 1, 1, 1, 0, 0])
    noisy_q = q + res*noise
    orig_ind = np.arange(q_len)
    ind = np.argsort(noisy_q)[::-1]
    sorted_noisy_q = noisy_q[ind]
    sorted_orig_ind = orig_ind[ind]
    # print("before loop: noisy_q={}, sorted_q={}, sorted_ind={}".format(noisy_q, sorted_noisy_q, sorted_orig_ind))
    pr1.disable()
    s1 = io.StringIO()
    sortby = SortKey.CUMULATIVE
    ps1 = pstats.Stats(pr1, stream=s1).sort_stats(sortby)
    ps1.print_stats()
    
    pr2.enable()
    tie = False
    for i in range(k+1):
        if sorted_noisy_q[i] == sorted_noisy_q[i+1]:
            tie = True
            break

    # loop to break ties
    while(tie):
        tie = False
        res = res/m
        x = x/m
        # eliminate queries that are not among top k+2
        q_len = len(sorted_noisy_q)
        if q_len > k + 2:
            for i in range(k + 1, q_len - 1):
                if sorted_noisy_q[i] > sorted_noisy_q[i+1]:
                    # ind = ind[:i+1]
                    sorted_orig_ind = sorted_orig_ind[:i+1]
                    sorted_noisy_q = sorted_noisy_q[:i+1]
                    break
        # print("in loop 1: sorted_q={}, sorted_ind={}".format(sorted_noisy_q, sorted_orig_ind))
        noise = np.array([geometric_exp(x) for i in range(len(sorted_noisy_q))])
        sorted_noisy_q = sorted_noisy_q + res*(noise % m)
        # print("Loop: t = {}, noisy_q = {}".format(t,noisy_q))
        ind = np.argsort(sorted_noisy_q)[::-1]
        sorted_orig_ind = sorted_orig_ind[ind]
        sorted_noisy_q = sorted_noisy_q[ind]
        # print("in loop 2: noise={}, sorted_q={}, sorted_ind={}".format(noise, sorted_noisy_q, sorted_orig_ind))

        # check for ties again
        for i in range(k+1):
            if sorted_noisy_q[i] == sorted_noisy_q[i+1]:
                tie = True
                break

    pr2.disable()
    s2 = io.StringIO()
    sortby = SortKey.CUMULATIVE
    ps2 = pstats.Stats(pr2, stream=s2).sort_stats(sortby)
    ps2.print_stats()

    pr3.enable()
    # compute gaps
    y = np.random.permutation(k+1)
    gap = []
    for i in range(k):
        if y[i] < y[i+1]:
            gap.append(np.floor((sorted_noisy_q[i]-sorted_noisy_q[i+1]-res)/target_res)*target_res)
        else:
            gap.append(np.floor((sorted_noisy_q[i]-sorted_noisy_q[i+1])/target_res)*target_res)
    # return sorted_orig_ind[:k], gap

    pr3.disable()
    s3 = io.StringIO()
    sortby = SortKey.CUMULATIVE
    ps3 = pstats.Stats(pr3, stream=s3).sort_stats(sortby)
    ps3.print_stats()


    
    return s1, s2, s3


if __name__=='__main__':
    q = np.zeros(10000)
    k = 1000
    eps = Fraction(1,1)

    s1, s2, s3 = prof_noisy_top_k_secure_fast(q, k, eps)
    
    print(f's1={s1.getvalue()}\n')
    print(f's2={s2.getvalue()}\n')
    print(f's3={s3.getvalue()}\n')