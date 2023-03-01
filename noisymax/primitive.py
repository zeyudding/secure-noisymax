import random
import numpy as np
from math import floor
from fractions import Fraction


# sample int uniformly from 0,1,...,n-1
def uniform(n, rng=random.SystemRandom()):
    return rng.randrange(n)


# sample from a Bernoulli(p) distribution
# p is a Fraction object in [0,1]
def bernoulli(p, rng=random.SystemRandom()):
    n = uniform(p.denominator, rng)
    if n < p.numerator:
        return 1
    else:
        return 0


# sample from a Bernoulli(exp(-x)) distribution
# x is a Fraction object in [0,1]
def bernoulli_exp1(x, rng=random.SystemRandom()):
    k = 1
    while True:
        p = x/Fraction(k, 1)
        if bernoulli(p, rng) == 0:
            break
        else:
            k = k + 1
    return k%2


# sample from a Bernoulli(exp(-x)) distribution
# x is a Fraction object >= 0
def bernoulli_exp(x, rng=random.SystemRandom()):
    while x > 1:
        if bernoulli_exp1(Fraction(1,1), rng) == 0:
            return 0
        x = x - 1
    return bernoulli_exp1(x, rng)


# sample from a geometric(1-exp(-x)) distribution
# x is a Fraction object > 0
# slow when x is close to 0
def geometric_exp1(x, rng=random.SystemRandom()):
    k = 0
    while bernoulli_exp(x, rng) == 1:
        k = k + 1
    return k


# sample from a geometric(1-exp(-x)) distribution
# x is a Fraction object > 0
def geometric_exp(x, rng=random.SystemRandom()):
    t = x.denominator
    while True:
        u = uniform(t, rng)
        b = bernoulli_exp(Fraction(u, t), rng)
        if b == 1:
            break
    v = geometric_exp1(Fraction(1,1), rng)
    return (u + t*v)//x.numerator

