# from fractions import Fraction
import numpy as np
from noisymax.primitive import geometric_exp


# 
def noisy_top_k(q, k, eps_numerator, eps_denominator):
    '''
    The noisy_top_k_with-gap mechanism [Ding et al.]
        Parameters:
            q (np.ndarray): a list of queries
            k (int): number of queries to be returned
            eps (float): privacy budget
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

# def noisy_top_k_secure_fast1(q, k, eps, m=10, target_res=Fraction(1, 10)):
#     '''
#     The secure implementation of the noisy_top_k_with-gap mechanism 
#         Parameters:
#             q (np.ndarray): a list of queries
#             k (int): number of queries to be returned
#             eps (Fraction): privacy budget
#             m (int): resolution increase factor
#             target_res (Fraction): target resolution (precision) of query
#         Returns:
#             ind (List[int]): the indices of top-k queries
#             gap (List[int]): the gaps between top-(k+1) queries 
#     '''
#     x = eps*target_res/(2*k)
#     res = target_res
#     t = 1
#     tie = True
#     original_ind = np.arange(len(q))
#     noisy_q = q
#     # print("---START---")
#     while(tie):
#         noise = np.array([geometric_exp(x) for i in range(len(noisy_q))])
#         if t == 1:
#             noisy_q = noisy_q + res*noise
#         else:
#             noisy_q = noisy_q + res*(noise % m)
#         # print("Loop: t = {}, noisy_q = {}".format(t,noisy_q))
#         ind = np.argsort(noisy_q)[::-1]
#         original_ind = original_ind[ind]
#         noisy_q = noisy_q[ind]
#         # eliminate queries that are < top k + 2
#         q_len = len(noisy_q)
#         if q_len > k + 2:
#             for i in range(k + 1, q_len - 1):
#                 if noisy_q[i] > noisy_q[i+1]:
#                     ind = ind[:i+1]
#                     noisy_q = noisy_q[:i+1]
#                     break
#         # loop for checking ties
#         for i in range(k+1):
#             if noisy_q[i] == noisy_q[i+1]:
#                 tie = True
#                 res = res/m
#                 x = x/m
#                 t = t + 1
#                 break
#             else:
#                 tie = False
#     # compute gaps
#     y = np.random.permutation(k+1)
#     gap = []
#     for i in range(k):
#         if y[i] < y[i+1]:
#             # print("low")
#             gap.append(np.floor((noisy_q[i]-noisy_q[i+1]-res)/target_res)*target_res)
#         else:
#             # print("high")
#             gap.append(np.floor((noisy_q[i]-noisy_q[i+1])/target_res)*target_res)
#     return original_ind[:k], gap

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
    # curr_res_numerator, curr_res_denominator = res_numerator, res_denominator
    noise = np.array([geometric_exp(x_numerator, x_denominator) for i in range(l)])
    noisy_q = q + noise * curr_res
    # print("noise has type: {}, noisy_q has type: {}".format(type(noise[0]), type(noisy_q[0])))
    ind = np.argsort(noisy_q)[-(k+2):][::-1] # top k+2 indexes in descending order
    tie = False
    # print("x={}, noise={}, noisy_q={}".format(x, noise, noisy_q))
    for i in range(k+1):
        if noisy_q[ind[i]] == noisy_q[ind[i+1]]:
            tie = True
            break
    
    # loop to break ties
    while(tie):
        tie = False
        # curr_res_denominator *= m
        curr_res /= m
        x_denominator *= m
        noise = np.array([geometric_exp(x_numerator, x_denominator) for i in range(l)])
        noisy_q = noisy_q + (noise % m) * curr_res
        ind = np.argsort(noisy_q)[-(k+2):][::-1]
        # check for ties again
        # print("x={}, noise={}, noisy_q={}".format(x, noise, noisy_q))
        # print("noise has type: {}, noisy_q has type: {}".format(type(noise[0]), type(noisy_q[0])))
        for i in range(k+1):
            if noisy_q[ind[i]] == noisy_q[ind[i+1]]:
                tie = True
                break
    # print("res={}, target_res={}".format(res, target_res))
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
    # res = target_res
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
    # print("before loop: noisy_q={}, sorted_q={}, sorted_ind={}".format(noisy_q, sorted_noisy_q, sorted_orig_ind))

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
                    # ind = ind[:i+1]
                    sorted_orig_ind = sorted_orig_ind[:i+1]
                    sorted_noisy_q = sorted_noisy_q[:i+1]
                    break
        # print("in loop 1: sorted_q={}, sorted_ind={}".format(sorted_noisy_q, sorted_orig_ind))
        noise = np.array([geometric_exp(x_numerator, x_denominator) for i in range(len(sorted_noisy_q))])
        sorted_noisy_q = sorted_noisy_q + (noise % m) * curr_res
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

    # compute gaps
    y = np.random.permutation(k+1)
    gap = []
    for i in range(k):
        if y[i] < y[i+1]:
            gap.append(np.floor((sorted_noisy_q[i]-sorted_noisy_q[i+1]-curr_res)/res)*res)
        else:
            gap.append(np.floor((sorted_noisy_q[i]-sorted_noisy_q[i+1])/res)*res)
    return sorted_orig_ind[:k], gap