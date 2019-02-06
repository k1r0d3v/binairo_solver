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
    def from_values(size, values):
        t = Table()
        t.__size = size
        t.__data = list('.' * size * size)
        for i in values:
            t.__data[abs(i) - 1] = '0' if i < 0 else '1'
        return t

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
        cnf = Clasp._cnf_format(variable_count, clauses)
        # Execute clasp with cnf string as input
        cp = subprocess.run(
            ['clasp', '--verbose=0', '{0}'.format(max_solutions)], 
            input=cnf,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        stderr = str(cp.stderr, encoding='utf-8')
        stdout = str(cp.stdout, encoding='utf-8')

        # Raise a exception if stderr is not empty
        if len(stderr) != 0:
            raise Exception('{}\n{}'.format(cnf, stderr))

        # Parse the solutions
        result = None
        solutions = []
        lines = stdout.split('\n')
        row = []
        for line in lines:
            if line.startswith('v '):
                tmp = list(map(int, line[2:].split(' ')))

                # Only when the line ends with 0 is a full solution
                # else is a partial solution
                if tmp[-1] == 0:
                    row.extend(tmp[:-1])
                    solutions.append(row)
                    row = []
                else:
                    row.extend(tmp)

            elif line.startswith('s '):
                result = line[2:]
                break
        
        return solutions, result
    

# Generate prepositions for a row and a column
# given his index
def rule_2(size, index):
    assert size > 1, 'size too small'

    half = size // 2

    rows = []
    cols = []

    # Row index rules
    for i in range(index * size, index * size + size - half + 1):
        row = []
        for j in range(0,  half):
            row.append(i + j + 1)

        rows.append(row)
        rows.append(list(map(lambda x: -x, row)))

    # Column index rules
    for i in range(0, size - half + 1):
        col = []
        for j in range(0,  half):
            col.append((i + j) * size + index + 1)

        cols.append(col)
        cols.append(list(map(lambda x: -x, col)))

    rows.extend(cols)
    return rows


#
# Main
#

t = Table.from_file('sample.txt')
print(t)
print('')

size = 6
rules = []
for i in range(0, size):
    rules.extend(rule_2(size, i))

solutions, result = Clasp.resolve(
    size * size, # Number of variables
    rules,
    max_solutions=2
)

for i in range(0, len(solutions)):
    print('Test solution {}'.format(i))
    print(Table.from_values(size, solutions[i]))
    print('')