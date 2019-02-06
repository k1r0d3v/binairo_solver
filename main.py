#!/bin/python3

import subprocess
import sys
import math

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
    
    # Note: 
    # Negative values are white and
    # positive values are black
    #
    # white = 0 with values < 0
    # black = 1 with values > 0
    @staticmethod
    def from_values(values):
        t = Table()
        t.__size = int(math.sqrt(len(values))) # len(values) = size * size
        t.__data = list('.' * len(values)) # Fill data with empty chars
        
        for i in values:
            if (abs(i) - 1) > len(t.__data):
                raise Exception('index out of range: {} in [{}, {})'.format(abs(i), 0, len(t.__data)))
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


class Rules:
    def __init__(self, table):
        self.__table = table
        self.__clauses = []
        self.__size = table.size()

    def not_more_than_two(self):
        for i in range(0,self.__size-1):
            row = self.__table.getRow(i)
            for j in range(0,self.__size-3):
                num = i * self.__size + j + 1
                if row[j] == '0':
                    self.__clauses.append([num, num + 1, num + 2])
                elif row[j] == '1':
                    self.__clauses.append([- num, - num - 1, - num - 2])
                else:
                    self.__clauses.append([num, num + 1, num + 2])
                    self.__clauses.append([- num, - num - 1, - num - 2])

            column = self.__table.getColumn(i)      
            for j in range(0,self.__size-3):
                num = j * self.__size + i + 1
                if column[j] == '0':
                    self.__clauses.append([num, num + self.__size, num + self.__size * 2])
                elif column[j] == '1':
                    self.__clauses.append([- num, - num - self.__size, - num - self.__size * 2])
                else:
                    self.__clauses.append([num, num + self.__size, num + self.__size * 2])
                    self.__clauses.append([- num, - num - self.__size, - num - self.__size * 2])
    
    """def row_column_not_equals(self):
        for i in range(0,self.__size-1):"""


    def aplicate_rules(self):
        self.not_more_than_two()
        return self.__clauses


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
    

# Note: Negatives values are white and
# positive values are black
#
# white = 0 with values < 0
# black = 1 with values > 0
def rule_table(t):
    row = []
    
    for i, value in enumerate(t.data()):
        if value == '0':
            row.append([-(i + 1)])
        elif value == '1':
            row.append([i + 1])
    return row

def rule_1(size, index):
    pass

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
    
def rule_3(size):
    assert size > 1, 'size too small'
    
    clause = []
    
    for k in range(0, size - 1):
        for i in range(0, size - k - 1):
            row = []
            row.append([k * size + 1, (k + i + 1) * size + 1])
            row.append([-k * size - 1, -(k + i + 1) * size - 1])
            col = []
            col.append([k + 1, (k + i + 1) + 1])
            col.append([-k - 1, -(k + i + 1) - 1])
            for j in range(1,  size):
                aux=[]
                for count in range(0, len(row)):
                    clone=row[count].copy()
                    row[count].extend([k * size + j + 1, (k + i + 1) * size + j + 1])
                    clone.extend([-k * size -j - 1, -(k + i + 1) * size -j - 1])
                    aux.append(row[count])
                    aux.append(clone)

                    clone=col[count].copy()
                    col[count].extend([j * size + k + 1, j * size + k + i + 1])
                    clone.extend([-k * size - j - 1, - j * size - k - i - 1])
                    col.append(clone)
                row=aux
            clause.extend(row)
            clause.extend(col)
    return clause


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
rules.extend(rule_table(t))
rules.extend(rule_3(size))

solutions, result = Clasp.resolve(
    size * size, # Number of variables
    rules,
    max_solutions=2
)

for i in range(0, len(solutions)):
    print('Test solution {}'.format(i))
    print(Table.from_values(solutions[i]))
    print('')