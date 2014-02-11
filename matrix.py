#!/usr/bin/python3

import sys
import re

def multiply(matrix, other):
    multipliedMatrix = []
    for i in range(0, len(matrix)):
        multipliedMatrix.append([]);
        for j in range(0, len(other[1])):
            multipliedMatrix[i].append("");
            multipliedMatrix[i][j] = ""
            for k in range(0, len(matrix[1])):
                if k > 0 and matrix[i][k] != "0" and other[k][j] != "0":
                    multipliedMatrix[i][j] += " + "
                if (matrix[i][k] == "0" or other[k][j] == "0"):
                    if (k == 0):
                        multipliedMatrix[i][j] += "0"
                else:
                    multipliedMatrix[i][j] +=  "%s*%s" %(matrix[i][k], other[k][j])
            
    return multipliedMatrix

def list_tuple(one, two):
    if len(one) == len(two):
        return [(one[i], two[i]) for i in range(0, len(one))]
            

def add(matrix, other):
    addedMatrix = [["(%s+%s)" %(a, b) for a, b in list_tuple(c, d)] for c, d in list_tuple(matrix, other)]
    return addedMatrix

def evaluate(matrix):
    return [[eval(x) for x in a] for a in matrix]

def printLaTeX(matrix, outf=sys.stdout):
    print("\\begin{bmatrix}", file=outf)
    for i in range(0, len(matrix)):
        printstring = ""
        for j in range(0, len(matrix[1])):
            if j > 0:
                printstring += "&"
            printstring += str(matrix[i][j])

        if i < len(matrix) - 1:
            print(printstring + "\\\\", file=outf)
        else:
            print(printstring + "\\end{bmatrix}", file=outf)
