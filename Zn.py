#!/usr/bin/python3

from tools import *

class Zn:
    def __init__(self, n):
        self.n = n;
        self.field = True;

    def __call__(self, a):
        return amodn(a, self.n)

class amodn:
    def legalop(self, other):
        if isinstance(other, type(self)):
            return self.n == other.n
        return False

    def __init__(self, a, n):
        if type(n) == int:
            self.n = n
        elif type(n) == str:
            self.n = int(n)
        else:
            return None
        if type(a) == int:
            self.a = a % n
        elif type(a) == str:
            self.a = int(a) % n
        else:
            return None

    def __repr__(self):
        return "(%s, %s)" %(self.a, self.n)

    def __str__(self):
        return str(self.a)
    
    def __add__(self, other):
        if self.legalop(other):
            return amodn(self.a + other.a, self.n)
        elif type(other) == int:
            return amodn(self.a + other, self.n)
        else:
            return NotImplemented

    def __sub__(self, other):
        if self.legalop(other):
            return amodn(self.a - other.a, self.n)
        elif type(other) == int:
            return amodn(self.a - other, self.n)
        else:
            return NotImplemented

    def __mul__(self, other):
        if self.legalop(other):
            return amodn(self.a*other.a, self.n)
        elif type(other) == int:
            return amodn(self.a*other, self.n)
        else:
            return NotImplemented

    def __pow__(self, other):
        if self.legalop(other):
            return amodn(pow(self.a, other.a), self.n)
        elif type(other) == int:
            return amodn(self.a**other, self.n)
        else:
            return NotImplemented
    
    def __truediv__(self, other):
        if self.legalop(other) and coprime(other.a, other.n):
            return self*~other
        else:
            return NotImplemented

    def __neg__(self):
        return amodn(-self.a, self.n)

    def __pos__(self):
        return amodn(+self.a, self.n)

    def __abs__(self):
        return amodn(abs(self.a), self.n)

    def __invert__(self):
        if coprime(self.a, self.n):
            return amodn(self.a**(phi(self.n)-1), self.n)
        else:
            return NotImplemented

    def __complex__(self):
        return complex(self.a)

    def __int__(self):
        return int(self.a)

    def __float__(self):
        return float(self.a)

    def __round__(self, n=0):
        return round(self.a, n)

    def __index__(self):
        return self.a

    def __radd__(self, other):
        return self + other

    def __rsub__(self, other):
        return -(self - other)

    def __rmul__(self, other):
        return self*other

    def __rtruediv__(self, other):
        if self.legalop(other) and coprime(self.a, self.n):
            return amodn(other.a*(~self.a), self.n)
        elif type(other) == int and coprime(self.a, self.n):
            return amodn(other*(~self.a), self.n)
        else:
            return NotImplemented

    def __ge__(self, other):
        if self.legalop(other):
            return self.a >= other.a
        elif type(other) == int:
            return self.a >= other
        else:
            return NotImplemented

    def __eq__(self, other):
        if type(other) == int:
            return self.a == other
        return self >= other and other >= self

    def __le__(self, other):
        if type(other) == int:
            return self.a <= other
        return other >= self

    def __ne__(self, other):
        if type(other) == int:
            return self.a != other
        return not self == other

    def __lt__(self, other):
        if type(other) == int:
            return self.a < other
        return self <= other and self != other

    def __gt__(self, other):
        if type(other) == int:
            return self.a > other
        return other < self


class qf:
    def __init__(self, ring):
        self.ring = ring;
        self.field = True;

    def __call__(self, a):
        return quotient(a, self.ring)


class quotient:
    def legalop(self, other):
        if isinstance(other, type(self)):
            return self.ring == other.ring
        return False

    def lower_terms(self):
        g = gcd(self.contents[0], self.contents[1])
        if g != 1:
            self.contents = (self.ring(self.contents[0]/g), self.ring(self.contents[1]/g))

    def __init__(self, a, ring=int, already_lowest=False):
        self.ring = ring
        if type(a) == ring:
            self.contents = (a, 1)
        elif type(a) == tuple:
            if any(type(coef) != self.ring for coef in a):
                self.contents = tuple(self.ring(coef) for coef in a)
            else:
                self.contents = a
        if not already_lowest:
            self.lower_terms()

    def __repr__(self):
        if self.contents[1] != self.ring(1):
            return "(%s/%s)" %(self.contents[0], self.contents[1])
        else:
            return "%s" %(self.contents[0])

    def __str__(self):
        if self.contents[1] != self.ring(1):
            return "(%s/%s)" %(self.contents[0], self.contents[1])
        else:
            return "%s" %(self.contents[0])
    
    def __add__(self, other):
        if self.legalop(other):
            return quotient(qf_sumh(self.contents, other.contents), self.ring, True)
        elif type(other) == self.ring:
            return quotient(qf_sumh(self.contents, (other, 1)), self.ring, True)
        else:
            return NotImplemented

    def __sub__(self, other):
        if self.legalop(other):
            return self + (-other)
        elif type(other) == int:
            return self + (-other)
        else:
            return NotImplemented

    def __mul__(self, other):
        if self.legalop(other):
            return quotient(qf_multh(self.contents, other.contents)[:2], self.ring, True)
        elif type(other) == int:
            return quotient(qf_multh(self.contents, (other, 1))[:2], self.ring, True)
        else:
            return NotImplemented

    def __pow__(self, other):
        if type(other) == int:
            temp = quotient((self.ring(1), self.ring(1)), self.ring, True)
            for i in range(0, other):
                temp *= self
            return temp
        else:
            return NotImplemented
    
    def __truediv__(self, other):
        if self.legalop(other):
            return self*~other
        else:
            return NotImplemented

    def __neg__(self):
        return quotient((-self.contents[0], self.contents[1]), self.ring, True)

    def __pos__(self):
        return quotient((+self.contents[0], self.contents[1]), self.ring, True)

    def __abs__(self):
        return quotient((abs(self.contents[0]), abs(self.contents[1])), self.ring, True)

    def __invert__(self):
        return quotient((self.contents[1], self.contents[0]), self.ring, True)

    def __radd__(self, other):
        return self + other

    def __rsub__(self, other):
        return -(self - other)

    def __rmul__(self, other):
        return self*other

    def __rtruediv__(self, other):
        if self.legalop(other):
            return amodn(other.a*(~self.a), self.n)
        elif type(other) == self.ring:
            return amodn(other*(~self.a), self.n)
        else:
            return NotImplemented
    
    def eval(self):
        return self.contents[0]/self.contents[1]

    def __ge__(self, other):
        if self.legalop(other):
            return self.eval() >= other.eval()
        elif type(other) == int:
            return self.eval() >= other
        else:
            return NotImplemented

    def __eq__(self, other):
        if type(other) == int:
            return self.contents[0] == other and self.contents[1] == 1
        return self >= other and other >= self

    def __le__(self, other):
        if type(other) == int:
            return self.eval() <= other
        return other >= self

    def __ne__(self, other):
        if type(other) == int:
            return self.eval() != other
        return not self == other

    def __lt__(self, other):
        if type(other) == int:
            return self.eval() < other
        return self <= other and self != other

    def __gt__(self, other):
        if type(other) == int:
            return self.eval() > other
        return other < self

def CRA2(r1, r2, m1, m2):
    r1 = int(r1)
    r2 = int(r2)
    m1 = int(m1)
    m2 = int(m2)
    c = int(~amodn(m1, m2))
    #print("c =", c)
    r1p = r1 % m1
    #print("r1^\prime =", r1p)
    sigma = ((r2 - r1p)*c) % m2
    #print("\sigma =", sigma)
    r = r1p + sigma*m1
    return r


        
