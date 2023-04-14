import numpy as np
from noisymax.primitive import geometric_exp


# 
def noisy_top_k(q, k, eps_numerator, eps_denominator):
    '''
    The noisy_top_k_with-gap mechanism [Ding et al.]
        Parameters:
            q (np.ndarray): a list of queries
            k (int): number of queries to be returned
            eps = eps_numerator/eps_denominator: privacy budget
        Returns:
            ind (List[int]): the indices of top-k queries
            gap (List[int]): the gaps between top-(k+1) queries 
    '''
    l = len(q)
    # assert k < l
    eps = eps_numerator / eps_denominator
    noise = [np.random.exponential(2*k/eps) for i in range(l)]
    noisy_q = q + noise
    ind = np.argsort(noisy_q)[-(k+1):][::-1]
    gap = [noisy_q[ind[j]]-noisy_q[ind[j+1]] for j in range(k)]
    return ind[:k], gap


def noisy_top_k_secure(q, k, eps_numerator, eps_denominator, m=10, res_numerator=1, res_denominator=10):
    '''
    The secure implementation of the noisy_top_k_with-gap mechanism 
        Parameters:
            q (np.ndarray): a list of queries
            k (int): number of queries to be returned
            eps = eps_numerator/eps_denominator: privacy budget
            m (int): resolution increase factor
            res = res_numerator/res_denominator: target resolution (precision) of query
        Returns:
            ind (List[int]): the indices of top-k queries
            gap (List[int]): the gaps between top-(k+1) queries 
    '''
    l = len(q)
    # x = eps*target_res/(2*k)
    x_numerator = eps_numerator * res_numerator 
    x_denominator = eps_denominator * res_denominator * 2 * k
    res = res_numerator/res_denominator
    curr_res = res
    noise = np.array([geometric_exp(x_numerator, x_denominator) for i in range(l)])
    noisy_q = q + noise * curr_res
    ind = np.argsort(noisy_q)[-(k+2):][::-1] # top k+2 indexes in descending order
    tie = False
    for i in range(k+1):
        if noisy_q[ind[i]] == noisy_q[ind[i+1]]:
            tie = True
            break
    
    # loop to break ties
    while(tie):
        tie = False
        curr_res /= m
        x_denominator *= m
        noise = np.array([geometric_exp(x_numerator, x_denominator) for i in range(l)])
        noisy_q = noisy_q + (noise % m) * curr_res
        ind = np.argsort(noisy_q)[-(k+2):][::-1]
        # check for ties again
        for i in range(k+1):
            if noisy_q[ind[i]] == noisy_q[ind[i+1]]:
                tie = True
                break

    y = np.random.permutation(k+1)
    gap = []
    for i in range(k):
        if y[i] < y[i+1]:
            gap.append(np.floor((noisy_q[ind[i]]-noisy_q[ind[i+1]]-curr_res)/res)*res)
        else:
            gap.append(np.floor((noisy_q[ind[i]]-noisy_q[ind[i+1]])/res)*res)
    return ind[:k], gap


def noisy_top_k_secure_fast(q, k, eps_numerator, eps_denominator, m=10, res_numerator=1, res_denominator=10):
    '''
    Similar to noisy_top_k_secure() but with early query elimination 
    '''
    q_len = len(q)
    # x = eps*target_res/(2*k)
    x_numerator = eps_numerator * res_numerator 
    x_denominator = eps_denominator * res_denominator * 2 * k
    res = res_numerator/res_denominator
    curr_res = res
    noise = np.array([geometric_exp(x_numerator, x_denominator) for i in range(q_len)])
    noisy_q = q + noise * curr_res
    orig_ind = np.arange(q_len)
    ind = np.argsort(noisy_q)[::-1]
    sorted_noisy_q = noisy_q[ind]
    sorted_orig_ind = orig_ind[ind]

    tie = False
    for i in range(k+1):
        if sorted_noisy_q[i] == sorted_noisy_q[i+1]:
            tie = True
            break

    # loop to break ties
    while(tie):
        tie = False
        curr_res /= m
        x_denominator *= m
        # eliminate queries that are not among top k+2
        q_len = len(sorted_noisy_q)
        if q_len > k + 2:
            for i in range(k + 1, q_len - 1):
                if sorted_noisy_q[i] > sorted_noisy_q[i+1]:
                    sorted_orig_ind = sorted_orig_ind[:i+1]
                    sorted_noisy_q = sorted_noisy_q[:i+1]
                    break

        noise = np.array([geometric_exp(x_numerator, x_denominator) for i in range(len(sorted_noisy_q))])
        sorted_noisy_q = sorted_noisy_q + (noise % m) * curr_res
        ind = np.argsort(sorted_noisy_q)[::-1]
        sorted_orig_ind = sorted_orig_ind[ind]
        sorted_noisy_q = sorted_noisy_q[ind]

        # check for ties again
        for i in range(k+1):
            if sorted_noisy_q[i] == sorted_noisy_q[i+1]:
                tie = True
                break

    # compute gaps
    y = np.random.permutation(k+1)
    gap = []
    for i in range(k):
        if y[i] < y[i+1]:
            gap.append(np.floor((sorted_noisy_q[i]-sorted_noisy_q[i+1]-curr_res)/res)*res)
        else:
            gap.append(np.floor((sorted_noisy_q[i]-sorted_noisy_q[i+1])/res)*res)
    return sorted_orig_ind[:k], gap