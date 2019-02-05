#!/bin/python3

import subprocess
import sys

if (sys.version_info.major * 10 + sys.version_info.minor) < 35:
        raise Exception("Python 3.5 or a more recent version is required.")

class Table:
    def __init__(self, filename):
        with open(filename, 'r') as file:
            self.__size = int(file.readline())
            self.__data = []
            for line in file:
                line = line.replace('\n', '')
                line = line.replace(' ', '')
                for column in line:
                    self.__data.append(column)

    def size(self):
        return self.__size

    def data(self):
        return self.__data
    
    def getCell(self, x, y):
        assert x < self.__size and y < self.__size, 'Index overflow'
        return self.__data[y * self.__size + x]

    def setCell(self, x, y, value):
        assert x < self.__size and y < self.__size, 'Index overflow'
        assert len(value) == 1, 'Expected char value'
        assert value == '.' or value == '0' or value == '1', 'Invalid value, accepted values are: ".", "0", "1"'

        index = y * self.__size + x
        old = self.__data[index]
        self.__data[index] = value
        return old

    def getRow(self, y):
        assert y < self.__size, 'Index overflow'
        row = y * self.__size
        return self.__data[row:row + self.__size]

    def getColumn(self, x):
        assert x < self.__size, 'Index overflow'

        col = []
        for i in range(0, self.__size):
            col.append(self.getCell(x, i))
        return col

    def __str__(self):
        str = ''
        for i in range(0, self.__size * self.__size):
            if (i != 0 and i % self.__size == 0):
                str += '\n'
            str += self.__data[i]
        return str

class Clasp:
    @staticmethod
    def _cnf_format(n, p):
        """ Description
        Format a list of prepositions to clasp format.
        Ex.
        p cnf 3 2
        -1 -3 0
        -2 -3 0

        :param n: number of variables
        :param p: list of prepositions
        """    
        cnf = 'p cnf {0} {1}\n'.format(n, len(p))

        for i in p:
            for j in i:
                cnf += '{} '.format(j)
            cnf += '0\n'
        return cnf.encode('utf-8')

    @staticmethod
    def resolve(n, p, max_solutions=0):
        # Execute clasp with cnf string as input
        cp = subprocess.run(
            ['clasp', '--verbose=0', '{0}'.format(max_solutions)], 
            input=Clasp._cnf_format(n, p),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        stderr = str(cp.stderr, encoding='utf-8')
        stdout = str(cp.stdout, encoding='utf-8')

        # Raise a exception if stderr is not empty
        if len(stderr) != 0:
            raise Exception(stderr)

        # Parse the solutions
        solutions = []
        lines = stdout.split('\n')
        for line in lines:
            if line.startswith('v '):
                solutions.append(list(map(int, line[2:].split(' ')[:-1])))
            elif line.startswith('s '):
                break
        
        return solutions

#
# Main
#

t = Table('sample.txt')

print(t)

print('Rows test')

print(t.getRow(0))
print(t.getRow(1))
print(t.getRow(2))
print(t.getRow(3))
print(t.getRow(4))
print(t.getRow(5))

print('Columns text')

print(t.getColumn(0))
print(t.getColumn(1))
print(t.getColumn(2))
print(t.getColumn(3))
print(t.getColumn(4))
print(t.getColumn(5))

print('Clasp test')

solutions = Clasp.resolve(
    # Number of variables
    3, 

    # Preposition list
    [
        [-1, -3],
        [-2, -3],
    ]
)

print(solutions)
