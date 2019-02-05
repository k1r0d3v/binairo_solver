#!/bin/python3

import subprocess
import sys

if (sys.version_info.major * 10 + sys.version_info.minor) < 35:
        raise Exception("Python 3.5 or a more recent version is required.")

class Table:
    def __init__(self):
        self.__size = 0
        self.__date = None

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
    
    @staticmethod
    def from_text(size, text):
        t = Table()
        t.__size = size
        t.__data = []

        lines = text.split('\n')
        for line in lines:
            for column in line:
                t.__data.append(column)
        return t

    @staticmethod
    def from_file(filename):
        
        with open(filename, 'r') as file:
            size = int(file.readline())
            return Table.from_text(size, file.read())
        raise Exception()


class Clasp:
    @staticmethod
    def _cnf_format(variable_count, clauses):
        """ Description
        Format a list of prepositions to clasp format.
        Ex.
        p cnf 3 2
        -1 -3 0
        -2 -3 0
        """    
        cnf = 'p cnf {0} {1}\n'.format(variable_count, len(clauses))        

        for i in clauses:
            for j in i:
                cnf += '{} '.format(j)
            cnf += '0\n'

        return cnf.encode('utf-8')

    @staticmethod
    def resolve(variable_count, clauses, max_solutions=0):
        # Execute clasp with cnf string as input
        cp = subprocess.run(
            ['clasp', '--verbose=0', '{0}'.format(max_solutions)], 
            input=Clasp._cnf_format(variable_count, clauses),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        stderr = str(cp.stderr, encoding='utf-8')
        stdout = str(cp.stdout, encoding='utf-8')

        # Raise a exception if stderr is not empty
        if len(stderr) != 0:
            raise Exception(stderr)

        # Parse the solutions
        result = None
        solutions = []
        lines = stdout.split('\n')
        for line in lines:
            if line.startswith('v '):
                solutions.append(list(map(int, line[2:].split(' ')[:-1])))
            elif line.startswith('s '):
                result = line[2:]
                break
        
        return solutions, result

#
# Main
#

t = Table.from_file('sample.txt')
print(t)
print('')

solutions, result = Clasp.resolve(
    # Number of variables
    4,

    [
        # CNF (1 and -2) or (-1 and 2 and -3) or (-2 and 3 and -4) or (-3 and 4)
        [-1, -2, 4],
        [1, 2, 3, 4],
        [1, -3, -4],
        [-2, -3],

        # CNF -((1 and -2) or (-1 and 2 and -3) or (-2 and 3 and -4) or (-3 and 4))
        [1, 2, -4],
        [-1, -2, -3, -4],
        [-1, 3, 4],
        [2, 3],
    ],
    max_solutions=0
)

print(solutions)
print(result)
