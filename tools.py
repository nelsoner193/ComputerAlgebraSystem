#!/usr/bin/python3

import itertools
import math

class strring:
    def __init__(self, value):
        self.val = str(value)
        self.field = True;

    def __add__(self, other):
        if type(other) == int:
            return self + strring(other)
        return strring("(%s+%s)" %(self.val, other.val))

    def __radd__(self, other):
        return self + strring(other)

    def __sub__(self, other):
        if type(other) == int:
            return self + strring(other)
        return strring("(%s-%s)" %(self.val, other.val))

    def __rsub__(self, other):
        return -self + strring(other)

    def __mul__(self, other):
        if type(other) == int:
            return self * strring(other)
        elif type(other) == strring:
            return strring("%s*%s" %(self.val, other.val))
        else:
            return NotImplemented

    def __rmul__(self, other):
        return self*strring(other)

    def __truediv__(self, other):
        return strring("\\frac{%s}{%s}" %(self.val, other.val))

    def __pow__(self, other):
        if type(other) == int:
            return strring("(%s)^%s" %(self.val, other))

    def __call__(self, value):
        return strring(value)

    def __str__(self):
        return self.val

    def __repr__(self):
        return "strring(%s)" %(self.val)

class squareroot:
    def __init__(self, value):
        self.val = value

    def __mul__(self, other):
        if self.val == other.val:
            return self.val
        return squareroot(self.val*other.val)

    def __rmul__(self, other):
        return self*squareroot(other*other)

    def __truediv__(self, other):
        return squareroot(self.val/other.val)

    def __pow__(self, other):
        if type(other) == int:
            if other % 2 == 0:
                return self.val**(other/2)
            else:
                return squareroot(self.val**other)

    def __str__(self):
        return "\sqrt{%s}" %(self.val)

    def __repr__(self):
        return "squareroot(%s)" %(self.val)

    def __gt__(self, other):
        if type(other) == int:
            return self.val > other*other

class ntuple:
    def __init__(self, *args, ring=float):
        self.contents = args
        if any(type(item) != ring for item in self.contents):
            self.contents = tuple([ring(item) for item in self.contents])
        self.ring = ring

    def __str__(self):
        return str(tuple(str(item) for item in self.contents))

    def __repr__(self):
        return "ntuple" + str(self.contents)

    def __getitem__(self, key):
        return self.contents[key]

    def __setitem__(self, key, value):
        if type(value) == ring:
            self.contents[key] = value

    def __len__(self):
        return len(self.contents)

    def conjugate(self):
        return ntuple(*[item.conjugate() for item in self.contents], ring=self.ring)

    def __add__(self, other):
        if len(self.contents) == len(other.contents):
            return ntuple(*[self.contents[i] + other.contents[i] for i in range(0, len(self.contents))], ring=self.ring)

    def __sub__(self, other):
        if len(self.contents) == len(other.contents):
            return ntuple(*[self.contents[i] - other.contents[i] for i in range(0, len(self.contents))], ring=self.ring)

    def __mul__(self, other):
        if type(other) == self.ring:
            return ntuple(*[item * other for item in self.contents], ring=self.ring)
        if len(self.contents) == len(other.contents):
            return ntuple(*[self.contents[i] * other.contents[i] for i in range(0, len(self.contents))], ring=self.ring)

    def __rmul__(self, other):
        return self*other

    def __truediv__(self, other):
        if type(other) == self.ring:
            return ntuple(*[item / other for item in self.contents], ring=self.ring)
        if len(self.contents) == len(other.contents):
            return ntuple(*[self.contents[i] / other.contents[i] for i in range(0, len(self.contents))], ring=self.ring)

    def __floordiv__(self, other):
        if len(self.contents) == len(other.contents):
            return ntuple(*[self.contents[i] // other.contents[i] for i in range(0, len(self.contents))], ring=self.ring)

    def __mod__(self, other):
        if len(self.contents) == len(other.contents):
            return ntuple(*[self.contents[i] % other.contents[i] for i in range(0, len(self.contents))], ring=self.ring)

def gcd(*args):
    temp = None
    for arg in args:
        if temp == None:
            temp = arg
        else:
            while arg:
                temp, arg = arg, temp % arg
    return temp

def prime_factors(n):
    """ Return the prime factors of the given number. """
    factors = []
    lastresult = n
     
    # 1 is a special case
    if n == 1:
        return [1]
     
    while lastresult > 1:
        c = 2
        while lastresult % c > 0:
            c += 1
        factors.append(c)
        lastresult /= c

    return factors

def sieve_eratosthenes(limit):
    """ Return all the primes below (NOT INCLUDING) the specified limit. """
     
    numbers = []
    primes = []
     
    for i in range(2, limit):
        numbers.append(i)
     
    while True:
        if len(numbers) == 0:
            break
         
        prime = numbers[0]
        primes.append(prime)
        multiples = []
         
        for n in numbers:
            if n % prime == 0:
                multiples.append(n)
         
        for n in multiples:
            numbers.remove(n)
    return primes

def coprime(a,b):
    """return True if 'a' and 'b' are coprime.
    
    >>> coprime(35,64)
    True
    """
    
    return gcd(a,b) == 1

def quadratic(f):
    if f.deg() == 2:
        a = f.coef[2]
        b = f.coef[1]
        c = f.coef[0]
        return [((-b + math.sqrt(b*b - 4*a*c)), 2*a), ((-b - math.sqrt(b*b - 4*a*c)), 2*a)]

def phi(m):
    """calculate Euler's totient function using a primitive method.
    
    >>> phi(1)
    1
    >>> phi(10)
    4
    """

    if m == 1:
        return 1
    else:
        r = [n for n in range(1,m) if coprime(m,n)]
        return len(r)

def is_prime(n):
    return len(prime_factors(n)) == 1

def lcm(*args):
    """Return lcm of args."""
    temp = None
    for arg in args:
        if temp == None:
            temp = arg
        else:
            temp = temp * arg // gcd(temp, arg)
    return temp

def continuedFraction(x):
    EPSILON = 1.0/(2.0)**25;
    MAXLENGTH = 12;
    if (abs(x) <= EPSILON):
        return [0]
    exp = []#continued fraction expansion
    i = 0.0

    while len(exp) < MAXLENGTH:
        if x + EPSILON > 0:
            i = int(x + EPSILON)
        else:
            i = int(x + EPSILON) - 1
        exp.append(i)
        x = x - i
        if abs(x) < EPSILON:
            break
        x = 1.0/x;
    return exp;
    
def asFraction(x):
    #f = asFraction(3.5); #returns f = [7,2];
    try:
        test = int(x)
    except:
        return [None, None]
    if x < 0:
        sign = -1
        x = x * -1
    else:
        sign = 1
    exp = continuedFraction(x);
    frac = [exp.pop(),1]
    while len(exp) > 0:
        last = exp.pop()
        frac = [frac[1] + frac[0]*last, frac[0]]
    frac[0] *= sign
    return frac;


def qf_multc(a, b):
    a1, a2 = a[0], a[1]
    b1, b2 = b[0], b[1]
    raw_product = ((a1*b1), (a2*b2))
    common_factor = gcd(raw_product[0], raw_product[1])
    print(raw_product, common_factor)
    return (raw_product[0]/common_factor, raw_product[1]/common_factor)

def qf_multh(a, b, output=False):
    a1, a2 = a[0], a[1]
    b1, b2 = b[0], b[1]
    if a1 == 0 or b1 == 0:
        return (0, 1)
    d1 = gcd(a1, b2)
    d2 = gcd(b1, a2)
    if output:
        print("d1 = %s, d2 = %s" %(d1, d2))
    a1p = a1/d1
    b2p = b2/d1
    b1p = b1/d2
    a2p = a2/d2
    if output:
        print("a1p = %s, a2p = %s, b1p = %s, b2p = %s" %(a1p, a2p, b1p, b2p))
    return (a1p*b1p, a2p*b2p)

def lowest_terms(a):
    a1, a2 = a[0], a[1]
    g = gcd(a1, a2)
    return (int(a1/g), int(a2/g))

def qf_sumh(a, b):
    a1, a2 = a[0], a[1]
    b1, b2 = b[0], b[1]
    g = gcd(a2, b2)
    a2p = a2/g
    b2p = b2/g
    ep = a1*b2p + b1*a2p
    fp = a2*b2p
    h = gcd(ep, g)
    e = ep/h
    f = fp/h
    return (e, f, h)

def gcd_prs_prem(a, b):
    prs = []
    if a.deg() >= b.deg():
        prs.append(a.pp())
        prs.append(b.pp())
    else:
        prs.append(b.pp())
        prs.append(a.pp())
    d = gcd(a.cont(), b.cont())
    r = prs[-2].pmod(prs[-1])
    prs.append(r)
    while r.deg() > 0:
        r = prs[-2].pmod(prs[-1])
        prs.append(r)
    print(prs)
    return d*prs[-1].pp()

def gcd_prs_pprem(a, b):
    prs = []
    if a.deg() >= b.deg():
        prs.append(a.pp())
        prs.append(b.pp())
    else:
        prs.append(b.pp())
        prs.append(a.pp())
    d = gcd(a.cont(), b.cont())
    r = prs[-2].pmod(prs[-1])
    prs.append(r)
    while r.deg() > 0:
        r = prs[-2].pmod(prs[-1]).pp()
        prs.append(r)
    print(prs)
    return d*prs[-1].pp()

def euclidean_inner_product(w, z):
    print("w =", w, " z =", z)
    return sum([w[i]*z[i].conjugate() for i in range(0, len(w))])

def gram_schmidt(B, inner_product):
    onB = []
    for i in range(0, len(B)):
        ei = B[i]
        print("v%s =" %(i), ei)
        for j in range(0, i):
            cyc = inner_product(B[i], onB[j])
            print("<v%s, e%s> =" %(i, j), cyc)
            print("<v%s, e%s>e%s =" %(i, j, j), cyc*onB[j])
            ei -= cyc*onB[j]
        print("e%s =" %(i), ei)
        print("norm(e%s) =" %(i), math.sqrt(inner_product(ei, ei)))
        ei = ei / math.sqrt(inner_product(ei, ei))
        print("finally e%s =" %(i), ei)
        onB.append(ei)
    return onB


"""
from polynom import *
from tools import *
from Zn import *
f1 = make_polynom("x^8 + x^6 - 3x^4 - 3x^3 + 8x^2 + 2x - 5")
f2 = make_polynom("3x^6 + 5x^4 - 4x^2 - 9x + 21")
f1
f2

gcd_prs_prem(f1, f2)

F = qf(int)
g1 = f1.change_ring(F)
g2 = f2.change_ring(F)

def print_gcd(*args):
    temp = None
    for arg in args:
        if temp == None:
            temp = arg
        else:
            while arg:
                temp, arg = arg, temp % arg
                print(arg)
    return temp

print_gcd(g1, g2)
"""
