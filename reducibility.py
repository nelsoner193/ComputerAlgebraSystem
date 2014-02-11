#!/usr/bin/python3

from polynom import *
from Zn import *
from tools import *

def process(f):
    if type(f) == str:
        f = make_polynom(f)
    return f

def rational_root(f):
    f = process(f)
    if int(f.coef[-1]) != f.coef[-1] or int(f.coef[0]) != f.coef[0]:
        return "cannot apply"
    leading_term = int(f.coef[-1])
    constant = int(f.coef[0])
    numerators = [i for i in range(1, constant+1) if constant % i == 0]
    denominators = [i for i in range(1, leading_term+1) if leading_term % i == 0]
    numerators += [-i for i in numerators]
    for b, c in itertools.product(numerators, denominators):
        if f(b/c) == 0:
            return "reducible, with a root of %s/%s" %(b, c)
    return "inconclusive"

def reduce_p(f, p, output=True):
    f = process(f)
    if any(type(c) != int for c in f.coef) or f.coef[-1] % p == 0:
        return "cannot apply"
    F = Zn(p)
    g = polynom(f.coef, True, F)
    print(g)
    if f.deg() == 2 or f.deg() == 3:
        for i in range(0, p):
            if output:
                print("g(%s) = %s" %(F(i), g(F(i))))
            if g(F(i)) == 0:
                return "inconclusive"
        return "irreducible"
    else:
        for i in range(0, p):
            if output:
                print("g(%s) = %s" %(F(i), g(F(i))))
            if g(F(i)) == 0:
                return "inconclusive"
        for i in range(2, math.ceil((len(g.coef))/2)):
            for fn in itertools.product(*[[F(i) for i in range(0, p)] for q in range(0, i+1)]):
                if fn == tuple([F(0) for i in range(0, i+1)]) or fn[-1] == F(0):
                    continue
                h = polynom(list(fn), True, F)
                temp = divmod(g, h)
                if output:
                    print("%s = (%s)(%s) + (%s)" %(g, h, temp[0], temp[1]))
                if not temp[1]:
                    return "inconclusive"
        return "irreducible"

def reduce_through(f, limit):
    output = (input("Do you want output with that? ").lower().startswith("y"))
    primes = sieve_eratosthenes(limit)
    for prime in primes:
        if reduce_p(f, prime, output) == "irreducible":
            print("reduction mod %s:" %(prime), "irreducible")
            break
    else:
        print("not irreducible with any of the %s primes from 2 through %s" %(len(primes), limit))

def eisenstein(f):
    f = process(f)
    if any(type(c) != int for c in f.coef):
        return "cannot apply"
    limit = gcd(*f.coef[:-1])
    if limit == 1:
        return "inconclusive"
    if limit < 0:
        limit = -limit
    potential = prime_factors(limit)
    for prime in potential:
        if f.coef[-1] % prime != 0 and f.coef[0] % (prime*prime) != 0:
            return "irreducible with p = %s" %(prime)
    return "inconclusive"
        
def reducibility(f):
    f = process(f)
    rr = rational_root(f)
    print("rational root:", rr)
    print("eisenstein criterion:", eisenstein(f))
    if f.deg() == 2 or f.deg() == 3:
        if f.deg() == 2:
            q = quadratic(f)
            print("quadratic equation roots: %s/%s, %s/%s" %(q[0][0], q[0][1], q[1][0], q[1][1]))
        if not rr.startswith("reducible"):
            reduce_through(f, 702)
        else:
            print("skipping reduction mod p as we already know it is reducible.")
    else:
        if not rr.startswith("reducible"):
            if input("Are you sure you want to reduce mod p? ").lower().startswith("y"):
                reduce_through(f, 702)
            else:
                print("Yeah, that was probably a good idea.")
        else:
            print("skipping reduction mod p as we already know it is reducible.")
