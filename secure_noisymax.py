from fractions import Fraction
import numpy as np
from sampling_primitive import *


# 
def noisy_top_k(q, k, eps):
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
    # assert isinstance(q, np.ndarray)
    # assert isinstance(k, int)
    # assert all(isinstance(x, int) for x in q)
    l = len(q)
    # assert k < l
    # noise = np.random.exponential(scale=2*k/eps, size=l)
    noise = [np.random.exponential(2*k/eps) for i in range(l)]
    noisy_q = q + noise
    # print(q)
    # print(noisy_q)
    ind = np.argsort(noisy_q)[-(k+1):][::-1]
    gap = [noisy_q[ind[j]]-noisy_q[ind[j+1]] for j in range(k)]
    return ind[:k], gap


def noisy_top_k_secure1(q, k, eps, m=10, target_res=Fraction(1, 10)):
    '''
    The secure implementation of the noisy_top_k_with-gap mechanism 
        Parameters:
            q (np.ndarray): a list of queries
            k (int): number of queries to be returned
            eps (Fraction): privacy budget
            m (int): resolution increase factor
            target_res (Fraction): target resolution (precision) of query
        Returns:
            ind (List[int]): the indices of top-k queries
            gap (List[int]): the gaps between top-(k+1) queries 
    '''
    l = len(q)
    x = eps*target_res/(2*k)
    noise = np.array(target_res*[geometric_exp(x) for i in range(l)])
    noisy_q = q + noise
    res = target_res
    tie = True
    while(tie):
        res = res/m
        x = x/m
        noise = np.array(
            [res*(geometric_exp(x) % m) for i in range(l)])
        noisy_q = noisy_q + noise
        ind = np.argsort(noisy_q)[-(k+2):][::-1]
        for i in range(k+1):
            if noisy_q[ind[i]] == noisy_q[ind[i+1]]:
                tie=True
                break
            else:
                tie = False
    # print("res={}, target_res={}".format(res, target_res))
    y = np.random.permutation(k+1)
    gap = []
    for i in range(k):
        if y[i] < y[i+1]:
            # print("low")
            gap.append(np.floor((noisy_q[ind[i]]-noisy_q[ind[i+1]]-res)/target_res)*target_res)
        else:
            # print("high")
            gap.append(np.floor((noisy_q[ind[i]]-noisy_q[ind[i+1]])/target_res)*target_res)
    # print(noisy_q)
    # print(ind)
    # print(noisy_q[ind])
    # print(gap)
    return ind[:k], gap


#
def noisy_top_k_secure(q, k, eps, m=10, target_res=Fraction(1, 10)):
    '''
    The secure implementation of the noisy_top_k_with-gap mechanism 
        Parameters:
            q (np.ndarray): a list of queries
            k (int): number of queries to be returned
            eps (Fraction): privacy budget
            m (int): resolution increase factor
            target_res (Fraction): target resolution (precision) of query
        Returns:
            ind (List[int]): the indices of top-k queries
            gap (List[int]): the gaps between top-(k+1) queries 
    '''
    l = len(q)
    x = eps*target_res/(2*k)
    res = target_res
    t = 1
    tie = True
    while(tie):
        noise = np.array([geometric_exp(x) for i in range(l)])
        if t == 1:
            noisy_q = q + res*noise
        else:
            noisy_q = noisy_q + res*(noise % m)
        ind = np.argsort(noisy_q)[-(k+2):][::-1]
        # loop for ties
        for i in range(k+1):
            if noisy_q[ind[i]] == noisy_q[ind[i+1]]:
                res = res/m
                x = x/m
                t = t + 1
                break
            else:
                tie = False
    # print("res={}, target_res={}".format(res, target_res))
    y = np.random.permutation(k+1)
    gap = []
    for i in range(k):
        if y[i] < y[i+1]:
            # print("low")
            gap.append(np.floor((noisy_q[ind[i]]-noisy_q[ind[i+1]]-res)/target_res)*target_res)
        else:
            # print("high")
            gap.append(np.floor((noisy_q[ind[i]]-noisy_q[ind[i+1]])/target_res)*target_res)
    # print(t)
    # print(noisy_q)
    # print(ind)
    # print(noisy_q[ind])
    # print(gap)
    return ind[:k], gap



def noisy_top_k_secure_fast(q, k, eps, m=10, target_res=Fraction(1, 10)):
    '''
    The secure implementation of the noisy_top_k_with-gap mechanism 
        Parameters:
            q (np.ndarray): a list of queries
            k (int): number of queries to be returned
            eps (Fraction): privacy budget
            m (int): resolution increase factor
            target_res (Fraction): target resolution (precision) of query
        Returns:
            ind (List[int]): the indices of top-k queries
            gap (List[int]): the gaps between top-(k+1) queries 
    '''
    x = eps*target_res/(2*k)
    res = target_res
    t = 1
    tie = True
    original_ind = np.arange(len(q))
    noisy_q = q
    # print("---START---")
    while(tie):
        noise = np.array([geometric_exp(x) for i in range(len(noisy_q))])
        if t == 1:
            noisy_q = noisy_q + res*noise
        else:
            noisy_q = noisy_q + res*(noise % m)
        # print("Loop: t = {}, noisy_q = {}".format(t,noisy_q))
        ind = np.argsort(noisy_q)[::-1]
        original_ind = original_ind[ind]
        noisy_q = noisy_q[ind]
        # eliminate queries that are < top k + 2
        q_len = len(noisy_q)
        if q_len > k + 2:
            for i in range(k + 1, q_len - 1):
                if noisy_q[i] > noisy_q[i+1]:
                    ind = ind[:i+1]
                    noisy_q = noisy_q[:i+1]
                    break
        # loop for checking ties
        for i in range(k+1):
            if noisy_q[i] == noisy_q[i+1]:
                res = res/m
                x = x/m
                t = t + 1
                break
            else:
                tie = False
    # compute gaps
    y = np.random.permutation(k+1)
    gap = []
    for i in range(k):
        if y[i] < y[i+1]:
            # print("low")
            gap.append(np.floor((noisy_q[i]-noisy_q[i+1]-res)/target_res)*target_res)
        else:
            # print("high")
            gap.append(np.floor((noisy_q[i]-noisy_q[i+1])/target_res)*target_res)
    # print("----END----")
    # print("res={}, target_res={}".format(res, target_res))
    # print("Total # of iteration: {}".format(t))
    # print(noisy_q)
    # print(ind)
    # print(noisy_q[:k+2])
    # print(gap)
    return original_ind[:k], gap