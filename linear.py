#!/usr/bin/python3

import itertools
import re

class matrix:
    def process(self):
        self.width = max([len(row) for row in self.contents])            
        for row in self.contents:
            for i, element in enumerate(row):
                if type(element) != type(self.ring(1)):
                    row[i] = self.ring(element)
            while len(row) < self.width:
                row.append(self.ring(0))

    def __init__(self, elements, ring=int):
        self.ring = ring
        if type(elements) == list:
            if type(elements[0]) == list:
                self.contents = elements
        elif type(elements) == str:
            elements = elements.strip()
            self.contents = []
            elements = elements.strip("\\\begin{bmatrx}ed")
            elements = re.sub("\\\\\\\\", "\\\\", elements)
            for row in elements.split("\\"):
                self.contents.append([self.ring(a) for a in row.split("&")])
        self.process()

        
    def __len__(self):
        return len(self.contents)

    def __repr__(self):
        retstring = "\\begin{bmatrix} "
        for i, row in enumerate(self.contents):
            if i > 0:
                retstring += " \\\\ "
            for j, element in enumerate(row):
                if j > 0:
                    retstring += " & "
                retstring += "%s" %(element)
        retstring += " \\end{bmatrix}"
        return retstring

    def __str__(self):
        max_width = max([len(str(i)) for i in itertools.chain(*[row for row in self.contents])])
        retstring = ""
        for i, row in enumerate(self.contents):
            if i > 0:
                retstring += "\n"
            retstring += "["
            for j, element in enumerate(row):
                if j > 0:
                    retstring += ", "
                elem = str(element)
                while len(elem) < max_width:
                    elem = " " + elem
                retstring += elem
            retstring += "]"
        return retstring

    def __add__(self, other):
        if type(other) == matrix:
            if len(self) == len(other) and self.width == other.width:
                return matrix([[a + b for a, b in zip(self.contents[i], other.contents[i])] for i in range(0, len(self))], ring=self.ring)

    def __mul__(self, other):
        if type(other) not in [matrix, int, float]:
            return NotImplemented
        multipliedMatrix = []
        for i in range(0, len(self)):
            multipliedMatrix.append([]);
            for j in range(0, len(other.contents[0])):
                multipliedMatrix[i].append(self.ring(0));
                multipliedMatrix[i][j] = self.ring(0)
                for k in range(0, len(self.contents[0])):
                    multipliedMatrix[i][j] +=  self.contents[i][k]*other.contents[k][j]
            
        return matrix(multipliedMatrix, ring=self.ring)
