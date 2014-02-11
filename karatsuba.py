 #!/usr/bin/python3

import math
from polynom import *

def int_len(n):
    digits = int(math.log10(abs(n)))+1
    return digits

def karatsuba(a, b):
    if type(a) == int and type(b) == int:
        n = max(int_len(a), int_len(b))
        m = int(n/2)
        base = 10
        basem = base**m
        a1 = int(a/basem)
        a0 = a%basem
        b1 = int(b/basem)
        b0 = b%basem
        z2 = a1*b1
        z0 = a0*b0
        z1 = (a1 + a0)*(b1 + b0) - z2 - z0
        return z2*(base**(2*m)) + z1*basem + z0
    if type(a) == polynom and type(b) == polynom:
        if not len(a) or not len(b):
            return polynom(0)
        n = max(len(a), len(b))
        m = int(n/2)
        a1 = a >> m
        a0 = polynom(a.coef[0:m], True, a.ring)
        b1 = b >> m
        b0 = polynom(b.coef[0:m], True, b.ring) 
        z2 = a1*b1
        z0 = a0*b0
        z1 = (a1 + a0)*(b1 + b0) - z2 - z0
        return (z2 << 2*m) + (z1 << m) + z0
