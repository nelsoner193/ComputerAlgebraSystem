#!/usr/bin/python3

def binom(n, k):
    print("n =", n, "and k =", k)
    if k == 0:
        print(1)
        return 1
    elif n == 0:
        print(0)
        return 0
    else:
        result = binom(n-1, k-1) + binom(n-1, k)
        print(result)
        return result

def string_binom(n, k):
    if k == 0:
        return "binom(%s, %s)" %(n, k)
    elif n == 0:
        return "binom(%s, %s)" %(n, k)
    else:
        return string_binom(n-1, k-1) + " + " + string_binom(n-1, k)
