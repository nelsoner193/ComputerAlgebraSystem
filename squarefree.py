#!/usr/bin/python3

from polynom import *
from mod_gcd import *

def squarefree(a):
    alist = [a]
    clist = []
    while len(clist) == 0 or len(clist[-1].coef) > 1:
        if type(a.coef[0]) != int:
            alist.append(gcd(alist[-1], alist[-1].derivative()))
        else:
            if alist[-1].deg() > 0:
                alist.append(mod_gcd(alist[-1], alist[-1].derivative()))
            else:
                alist.append(gcd(alist[-1].coef[0], alist[-1].derivative().coef[0]))
        c = alist[-2]/alist[-1]
        clist.append(c)
        print("alist =", alist)
        print("clist =", clist)

    blist = []
    for i in range(1, len(clist)):
        blist.append(clist[i-1]/clist[i])
    return blist
