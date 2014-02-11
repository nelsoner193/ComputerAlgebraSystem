#!/usr/bin/python3

import itertools
import re
from tools import strring, gcd
from pseudodivision import divp

def translate(polynomial_string):
    polynomial_string = re.sub("\^", "**", polynomial_string)
    polynomial_string = re.sub("(?<=\d)(?=x)", "*", polynomial_string)
    return polynomial_string

def make_polynom(polynomial_string, ring=int):
    x = indeterminate(ring=ring)
    f = eval(translate(polynomial_string)) # I know this is bad practice, but this was intended for importing into the Python interpreter and then being used interactively.
    if type(f) == indeterminate:
        return polynom([ring(0) for i in range(0, f.power)] + [f.coef], True, ring)
    elif type(f) == polynom:
        return f
    elif type(f) == ring:
        return polynom([ring(f)], True, ring)

class indeterminate:
    def __init__(self, coef=1, power=1, letter="x", ring=int):
        self.letter = letter
        self.ring = ring
        if coef == 1:
            self.coef = self.ring(1)
        else:
            if type(coef) == type(self.ring(1)):
                self.coef = coef
            else:
                self.coef = self.ring(coef)
        self.power = power

    def set_coef(self, a):
        if type(a) == type(self.coef):
            self.coef = a
        else:
            try:
                self.coef = ring(a)
            except:
                pass

    def __add__(self, other):
        if type(other) == indeterminate:
            if other.power == self.power:
                return indeterminate(self.coef+other.coef, self.power, ring=self.ring)
            else:
                coefs = [self.ring(0) for i in range(0, max(self.power, other.power)+1)]
                coefs[self.power] = self.coef
                coefs[other.power] = other.coef
                return polynom(coefs, True, self.ring)
        elif type(other) == self.ring:
            return self + indeterminate(self.ring(other), 0, ring=self.ring)
        elif type(other) == int:
            return self + indeterminate(self.ring(other), 0, ring=self.ring)
        else:
            return NotImplemented

    def __sub__(self, other):
        if type(other) == indeterminate or type(other) == self.ring or type(other) == int:
            return self + (-other)
        else:
            return NotImplemented

    def __neg__(self):
        return indeterminate(-self.coef, self.power, ring=self.ring)

    def __mul__(self, other):
        if type(other) == indeterminate:
            return indeterminate(self.coef*other.coef, self.power+other.power, ring=self.ring)
        elif type(other) == type(self.coef):
            return indeterminate(self.coef*other, self.power, ring=self.ring)
        elif type(other) == self.ring:
            return indeterminate(self.coef*other, self.power, ring=self.ring)
        elif type(other) == int:
            return indeterminate(self.coef*self.ring(other), self.power, ring=self.ring)
        else:
            return NotImplemented

    def __radd__(self, other):
        return self+other

    def __rmul__(self, other):
        return self*other

    def __pow__(self, other):
        if type(other) == int:
            return indeterminate(self.coef, self.power*other, ring=self.ring)
        else:
            return NotImplemented

    def __repr__(self):
        if self.power == 0:
            return str(self.coef)
        coef = ""
        power = ""
        if self.coef != self.ring(1):
            coef = str(self.coef)
        if self.power != 1:
            power = "^" + str(self.power)
        return "%s%s%s" %(coef, self.letter, power)

class polynom:
    def process(self):
        if any(type(i) != type(self.ring(0)) for i in self.coef):
            self.coef = [self.ring(i) for i in self.coef]
        while len(self.coef) > 1 and self.coef[-1] == self.ring(0):
            self.coef = self.coef[0:-1]

    def is_monic(self):
        return self.coef[-1] == self.ring(1)

    def __init__(self, coefficients, direct=False, ring=int):
        self.ring = ring
        if type(coefficients) == list:
            if direct:
                self.coef = coefficients
            else:
                self.coef = list(reversed(coefficients))
        elif type(coefficients) == str:
            self.coef = make_polynom(coefficients, self.ring).coef
                    
        self.process()

    def deg(self):
        if len(self.coef) == self.ring(1) and self.coef[0] == self.ring(0):
            return None
        return len(self.coef)-1

    def __add__(self, other):
        if type(other) == polynom:
            if len(self.coef) < len(other.coef):
                return other + self
            else:
                coef = self.coef
                for i in range(0, len(other.coef)):
                    coef[i] += other.coef[i]
                return polynom(coef, True, self.ring)
        elif type(other) == indeterminate:
            if other.power >= len(self.coef):
                coef = self.coef + [self.ring(0) for i in range(0, other.power - len(self.coef))] + [other.coef]
                return polynom(coef, True, self.ring)
            else:
                coef = self.coef
                coef[other.power] += other.coef
                return polynom(coef, True, self.ring)
        elif type(other) == int:
            coef = self.coef
            coef[0] += self.ring(other)
            return polynom(coef, True, self.ring)
        else:
            return NotImplemented
        
    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return self + -other

    def __neg__(self):
        return self*-1

    def __mul__(self, other):
        if type(other) == int or all(type(other) == type(coef) for coef in self.coef):
            return polynom([other*c for c in self.coef], True, self.ring)
        elif type(other) == type(self):
            coef = [self.ring(0) for i in range(0, len(self.coef)+len(other.coef))]
            for a, b in itertools.product(range(0, len(self.coef)), range(0, len(other.coef))):
                coef[a+b] += self.coef[a]*other.coef[b]
            return polynom(coef, True, self.ring)
        elif type(other) == indeterminate:
            return polynom([self.ring(0) for i in range(0, other.power)] + [other.coef*c for c in self.coef], True, self.ring)
        elif type(other) == float and all(type(coef) in [int, float] for coef in self.coef):
            return polynom([other*c for c in self.coef], True, self.ring)
        else:
            return NotImplemented

    def __rmul__(self, other):
        return self*other

    def __divmod__(self, other):
        if type(other) == self.ring:
            other = polynom([other], ring=self.ring)
        if other.deg() == None:
            return [None, None]
        if len(self.coef) < len(other.coef):
            return (polynom([1], True, self.ring), polynom(self.coef, True, self.ring))
        else:
            r = polynom(self.coef[:], True, self.ring)
            q = [self.ring(0) for i in range(0, len(self.coef))]
            while r.deg() != None and r.deg() >= other.deg():
                if "field" in self.ring.__dict__ or self.ring in [int, float]:
                    q[len(r.coef) - len(other.coef)] = r.coef[-1]/other.coef[-1]
                    r -= (other << r)*(r.coef[-1]/other.coef[-1])
                elif other.is_monic():
                    q[len(r.coef) - len(other.coef)] = r.coef[-1]
                    r -= (other << r)*(r.coef[-1])
                else:
                    return NotImplemented

            #print("q =", polynom(q, True, ring=self.ring), "and r =", r)
            return polynom(q, True, ring=self.ring), r

    def __floordiv__(self, other):
        return divmod(self, other)[0]

    def __mod__(self, other):
        return divmod(self, other)[1]

    def __truediv__(self, other):
        temp = divmod(self, other)
        if temp[1].deg() == None:
            return temp[0]
        else:
            return NotImplemented

    def __lshift__(self, other):
        if type(other) == int:
            return polynom([self.ring(0) for i in range(0, other)] + self.coef, True, self.ring)
        elif type(other) == polynom:
            return polynom([self.ring(0) for i in range(len(other.coef) - len(self.coef))] + self.coef, True, self.ring)
        else:
            return NotImplemented

    def __rshift__(self, other):
        if type(other) == int:
            if other >= 0:
                return polynom(self.coef[other:], True)
        elif type(other) == polynom:
            if len(self.coef) > len(other.coef):
                return polynom(self.coef[len(self.coef)-len(other.coef):], True)
        return NotImplemented

    def __pow__(self, other):
        if type(other) == int:
            if other >= 0:
                prod = polynom([self.ring(1)])
                for i in range(0, other):
                    prod *= self
                return prod
        return NotImplemented

    def __str__(self):
        if not self:
            return "0"
        representation = ""
        sep = ""
        for n, i in reversed(list(enumerate(self.coef))):
            if i != 0:
                if sep:
                    if type(i) == strring or i > 0:
                        representation += sep
                    else:
                        representation += " - "
                        i *= -1
                if n >= 2:
                    if i != 1:
                        representation += "%s%s%s" %(i, "x^", n)
                    else:
                        representation += "%s%s" %("x^", n)
                elif n == 1:
                    if i != 1:
                        representation += "%s%s" %(i, "x")
                    else:
                        representation += "x"
                else:
                    representation += "%s" %(i)
                sep = " + "
        return representation

    def __repr__(self):
        return str(self)

    def __len__(self):
        if len(self.coef) == 1 and self.coef[0] == 0:
            return 0
        return len(self.coef)

    def __call__(self, a):
        if all(type(coef) == int for coef in self.coef) and type(a) in [int, float]:
            return sum([self.coef[i]*(a**i) for i in range(0, len(self.coef))])
        elif all(type(a) == type(coef) for coef in self.coef):
            return sum([self.coef[i]*(a**i) for i in range(0, len(self.coef))])
        elif type(a) == polynom:
            return sum([self.coef[i]*(a**i) for i in range(0, len(self.coef))])
        else:
            return NotImplemented

    def __eq__(self, a):
        if type(a) == polynom:
            if self.deg() == a.deg():
                return self.ring == a.ring and all(self.coef[i] == a.coef[i] for i in range(0, len(self.coef)))
        if type(a) == type(self.ring):
            if not self.deg() and a == self.ring(0):
                return True
            if self.deg() == 0:
                return self.coef[0] == a
        return False

    def derivative(self):
        ad_coefs = [i*a for i, a in enumerate(self.coef)][1:]
        if len(ad_coefs) == 0:
            ad_coefs = [self.ring(0)]
        return polynom(ad_coefs, True, self.ring)

    def antiderivative(self):
        ad_coefs = [self.ring(0)] + [a/self.ring(i+1) for i, a in enumerate(self.coef)]
        ad = polynom(ad_coefs, True, self.ring)
        return ad

    def integral(self, a, b):
        ad = self.antiderivative()
        if a != 0:
            return ad(self.ring(b)) - ad(self.ring(a))
        else:
            return ad(self.ring(b))

    def pdivmod(self, other):
        if self.deg() < other.deg():
            raise Exception("a has to have degree greater than or equal to b's.")
        if self.ring != other.ring:
            raise Exception("a and b have to be polynomials over the same ring.")
        q = []
        ap = self
        c = other.coef[-1]
        m = ap.deg()
        n = other.deg()
        powers = [1, c]
        for i in range(2, m-n+1):
            powers.append(powers[-1]*c)
        loop_num = 1
        while m >= n:
            ap_norm = max([abs(coef) for coef in ap.coef])
            d = ap.coef[-1]*powers[m-n]
            q.append(d)
            ap = c*ap - ap.coef[-1]*(other << m-n) # This is b * x^{m-n}, I implemented multiplying by x^n as polynom << n.
            if not ap.deg():
                break
            for i in range(1, min(m - ap.deg() - 1, m - n) + 1):
                q.append(0)
                ap = c*ap
            m = ap.deg()
        q = polynom(q, ring=self.ring)
        r = ap
        return (q, r)

    def pfloordiv(self, other):
        return self.pdivmod(other)[0]

    def pmod(self, other):
        return self.pdivmod(other)[1]

    def cont(self):
        return gcd(*self.coef)

    def pp(self):
        c = self.cont()
        return polynom([coef/c for coef in self.coef], True, self.ring)

    def change_ring(self, ring):
        return polynom(self.coef[:], True, ring)
