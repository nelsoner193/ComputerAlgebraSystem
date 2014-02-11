#!/usr/bin/python3

from polynom import *
from Zn import *


def LandauMignotte(a, b):
    m = a.deg()
    n = b.deg()
    norm_a = math.sqrt(sum([coef*coef for coef in a.coef]))/a.coef[m]
    norm_b = math.sqrt(sum([coef*coef for coef in b.coef]))/b.coef[n]
    return 2**min(m, n) * gcd(a.coef[m], b.coef[n]) * min(norm_a, norm_b)

def mod_gcd(a, b):
    if a.ring != int or b.ring != int:
        return "Nope"
    #print("Step (1)")
    print(a, b)
    cont_a = gcd(*a.coef)
    cont_b = gcd(*b.coef)
    a = a / cont_a
    b = b / cont_b
    cont_gcd = gcd(cont_a, cont_b)
    #print(cont_gcd)
    d = gcd(a.coef[-1], b.coef[-1])
    M = 2*d*LandauMignotte(a, b)
    #print("d =", d)
    #print("M =", M)
    primes = sieve_eratosthenes(int(M+1))
    prime_index = 0
    while True:
        #print("Step (2)")
        while (a.coef[-1] % primes[prime_index] == 0 and b.coef[-1] % primes[prime_index] == 0):
            prime_index += 1
        p = primes[prime_index]
        prime_index += 1
        c_p = gcd(a.change_ring(Zn(p)), b.change_ring(Zn(p)))
        c_p = c_p*~c_p.coef[-1]
        g_p = (d % p)*c_p
        #print("with p =", p, "g_p =", g_p)
        while True:
            #print("Step (3)")
            if g_p.deg() == 0:
                return polynom([1])
            P = p
            g = g_p
            #print("P =", P, "and g =", g)
            #print("Step (4)")
            while P <= M:
                #print("P =", P)
                while (a.coef[-1] % primes[prime_index] == 0 or b.coef[-1] % primes[prime_index] == 0):
                    prime_index += 1
                p = primes[prime_index]
                prime_index += 1
                c_p = gcd(a.change_ring(Zn(p)), b.change_ring(Zn(p)))
                c_p = c_p*~c_p.coef[-1]
                g_p = (d % p)*c_p
                #print("with p =", p, "g_p =", g_p)
                if g_p.deg() < g.deg():
                    #print("New g_p has lower degree than the previous one.")
                    break
                if g_p.deg() == g.deg():
                    #print("Degrees match when p =", p)
                    g = polynom([CRA2(g.coef[i], g_p.coef[i], P, p) for i in range(0, len(g.coef))], True)
                    P *= p
                    #print("g =", g)
            else:
                #print("P =", P, "> M =", M, "so time to test for completion with g =", g)
                if any(coef > M for coef in g.coef):
                    #print("Positive coefficients are too large - we must have negative coefficients.")
                    coefs = []
                    for coef in g.coef:
                        if coef > M:
                            coefs.append(coef - P)
                        else:
                            coefs.append(coef)
                    alt_g = polynom(coefs, True)
                    if gcd(*alt_g.coef) != 1:
                        alt_g = alt_g/gcd(*alt_g.coef)
                        #print("Primitive part =", alt_g)
                    if not a % alt_g and not b % alt_g:
                        return cont_gcd*alt_g
                else:
                    if gcd(*g.coef) != 1:
                        g = g/gcd(*g.coef)
                        #print("Primitive part =", g)
                    if not a % g and not b % g:
                        return cont_gcd*g
                break

def mod_gcd2(a, b):
    if a.ring != int or b.ring != int:
        return "Nope"
    print("Step (1)")
    cont_a = gcd(*a.coef)
    cont_b = gcd(*b.coef)
    a = a / cont_a
    b = b / cont_b
    cont_gcd = gcd(cont_a, cont_b)
    print(cont_gcd)
    d = gcd(a.coef[-1], b.coef[-1])
    M = LandauMignotte(a, b)
    print("d =", d)
    print("M =", M)
    primes = sieve_eratosthenes(int(M+1))
    prime_index = 0
    while True:
        print("Step (2)")
        while (a.coef[-1] % primes[prime_index] == 0 and b.coef[-1] % primes[prime_index] == 0):
            prime_index += 1
        p = primes[prime_index]
        prime_index += 1
        c_p = gcd(a.change_ring(Zn(p)), b.change_ring(Zn(p)))
        c_p = c_p*~c_p.coef[-1]
        g_p = (d % p)*c_p
        print("with p =", p, "g_p =", g_p)
        while True:
            print("Step (3)")
            if g_p.deg() == 0:
                return polynom([1])
            P = p
            g = g_p
            print("P =", P, "and g =", g)
            print("Step (4)")
            while P <= M:
                print("P =", P)
                while (a.coef[-1] % primes[prime_index] == 0 or b.coef[-1] % primes[prime_index] == 0):
                    prime_index += 1
                p = primes[prime_index]
                prime_index += 1
                c_p = gcd(a.change_ring(Zn(p)), b.change_ring(Zn(p)))
                c_p = c_p*~c_p.coef[-1]
                g_p = (d % p)*c_p
                print("with p =", p, "g_p =", g_p)
                if g_p.deg() < g.deg():
                    print("New g_p has lower degree than the previous one.")
                    break
                if g_p.deg() == g.deg():
                    print("Degrees match when p =", p)
                    g = polynom([CRA2(g.coef[i], g_p.coef[i], P, p) for i in range(0, len(g.coef))], True)
                    P *= p
                    print("g =", g)
            else:
                print("P =", P, "> M =", M, "so time to test for completion with g =", g)
                if any(coef > M for coef in g.coef):
                    print("Positive coefficients are too large - we must have negative coefficients.")
                    coefs = []
                    for coef in g.coef:
                        if coef > M:
                            coefs.append(coef - P)
                        else:
                            coefs.append(coef)
                    alt_g = polynom(coefs, True)
                    if gcd(*alt_g.coef) != 1:
                        alt_g = alt_g/gcd(*alt_g.coef)
                        print("Primitive part =", alt_g)
                    if not a % alt_g and not b % alt_g:
                        return cont_gcd*alt_g
                else:
                    if gcd(*g.coef) != 1:
                        g = g/gcd(*g.coef)
                        print("Primitive part =", g)
                    if not a % g and not b % g:
                        return cont_gcd*g
                break

if __name__ == "__main__":
    import sys
    mod_gcd(make_polynom(sys.argv[1]), make_polynom(sys.argv[2]))
