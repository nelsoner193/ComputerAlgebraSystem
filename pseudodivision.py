from polynom import *
from math import log, floor

def divp(a, b):
    if a.deg() < b.deg():
        raise Exception("a has to have degree greater than or equal to b's.")
    if a.ring != b.ring:
        raise Exception("a and b have to be polynomials over the same ring.")
    print("$a(x) =", a, "$")
    print("$b(x) =", b, "$")
    l_num = max([abs(coef) for coef in a.coef + b.coef])
    l = floor(log(abs(l_num))) + 1
    #print("$l$ is the number of digits in $", l_num, "$, which is ", l)
    q = []
    ap = a
    c = b.coef[-1]
    m = ap.deg()
    n = b.deg()
    powers = [1, c]
    for i in range(2, m-n+1):
        powers.append(powers[-1]*c)
    loop_num = 1
    while m >= n:
        ap_norm = max([abs(coef) for coef in ap.coef])
        l_ap = floor(log(abs(ap_norm))) + 1
        #print("At the beginning of the %sth iteration through the loop, $\\norm[\\infty]{a^\\prime} =" %(loop_num), ap_norm, "$, with number of digits $", l_ap, "$ and it is", l_ap <= loop_num*l, "that $L(\\norm[\\infty]{a^\\prime})$ is $\O(il)$")
        #print("Also, $a^\\prime =", ap, "$")
        #print("And so far, $q =", polynom(q, ring=a.ring), "$")
        d = ap.coef[-1]*powers[m-n]
        #print("So $d =", d, "$")
        q.append(d)
        ap = c*ap - ap.coef[-1]*(b << m-n) # This is b * x^{m-n}, I implemented multiplying by x^n as polynom << n.
        for i in range(1, min(m - ap.deg() - 1, m - n) + 1):
            q.append(0)
            ap = c*ap
        m = ap.deg()
        loop_num += 1
    q = polynom(q, ring=a.ring)
    r = ap
    #print("Finally, we are left with $q =", q, "$ and $r =", r, "$")
    return (q, r)

def check_divp(a, b):
    m = a.deg()
    n = b.deg()
    c = (b.coef[-1])**(m-n+1)
    ca = c*a
    q, r = divp(a, b)
    print(ca)
    print(q*b + r)
    print("It is", ca == q*b + r, "that divp gives us the pseudoquotient and pseudoremainder.")

def generate_test_functions():
    from random import randint
    m = randint(10, 30)
    n = randint(2, m)
    f = polynom([randint(1, 10)] + [randint(-30, 30) for i in range(0, m)])
    g = polynom([randint(1, 10)] + [randint(-30, 30) for i in range(0, n)])
    return (f, g)

if __name__ == "__main__":
    for i in range(0, 1):
        check_divp(*generate_test_functions())
