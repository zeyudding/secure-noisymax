import random
import numpy as np
from math import floor
# from fractions import Fraction


# sample int uniformly from 0,1,...,n-1
def uniform(n, rng=random.SystemRandom()):
    return rng.randrange(n)


# sample from a Bernoulli(p) distribution
# p = p_numerator / p_denominator is in [0,1]
def bernoulli(p_numerator, p_denominator, rng=random.SystemRandom()):
    n = uniform(p_denominator, rng)
    if n < p_numerator:
        return 1
    else:
        return 0


# sample from a Bernoulli(exp(-x)) distribution
# x = x_numerator / x_denominator is in [0,1]
def bernoulli_exp1(x_numerator, x_denominator, rng=random.SystemRandom()):
    k = 1
    while True:
        # p = x/Fraction(k, 1)
        x_denominator *= k
        if bernoulli(x_numerator, x_denominator, rng) == 0:
            break
        else:
            k = k + 1
    return k%2


# sample from a Bernoulli(exp(-x)) distribution
# x = x_numerator / x_denominator is >= 0
def bernoulli_exp(x_numerator, x_denominator, rng=random.SystemRandom()):
    while x_numerator > x_denominator:
        if bernoulli_exp1(1, 1, rng) == 0:
            return 0
        # x = x - 1
        x_numerator -= x_denominator
    return bernoulli_exp1(x_numerator, x_denominator, rng)


# sample from a geometric(1-exp(-x)) distribution
# x is x_numerator / x_denominator > 0
# slow when x is close to 0
def geometric_exp1(x_numerator, x_denominator, rng=random.SystemRandom()):
    k = 0
    while bernoulli_exp(x_numerator, x_denominator, rng) == 1:
        k = k + 1
    return k


# sample from a geometric(1-exp(-x)) distribution
# x is x_numerator / x_denominator > 0
def geometric_exp(x_numerator, x_denominator, rng=random.SystemRandom()):
    # t = x.denominator
    # while True:
    #     u = uniform(t, rng)
    #     b = bernoulli_exp(Fraction(u, t), rng)
    #     if b == 1:
    #         break
    # v = geometric_exp1(Fraction(1,1), rng)
    # return (u + t*v)//x.numerator
    while True:
        u = uniform(x_denominator, rng)
        b = bernoulli_exp(u, x_denominator, rng)
        if b == 1:
            break
    v = geometric_exp1(1, 1, rng)
    return (u + x_denominator*v)//x_numerator

