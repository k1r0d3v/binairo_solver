#!/bin/python3

import subprocess
import sys
import math
import itertools

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

def rule_1_base(rows, row, col, cnt, size, offset):
    if len(row) == size and cnt != 0:
        return

    if len(row) == size:
        rows.append(row)
        rows.append(col)
        return

    if cnt != 0:
        rule_1_base(rows, row + [len(row) + 1 + offset * size], col + [len(col) * size + 1 + offset], cnt - 1, size, offset)

    rule_1_base(rows, row + [-(len(row) + 1 + offset * size)], col + [-(len(col) * size + 1 + offset)], cnt, size, offset)

# TODO: Explain
#
# Cases not in permutations of
# |0|0|0|1|1|1|
#
def rule_1(size, index):
    cnt = size // 2
    rows = []
    for i in range(0, cnt):
        rule_1_base(rows, [], [], i, size, index)

    tmp = rows.copy()
    tmp = list(map(lambda r: list(map(lambda x: -x, r)), tmp))

    rows.extend(tmp)
    return rows

# TODO: Explain
#
# |0|0|0|x|x|x|
# |x|0|0|0|x|x|
# |x|x|0|0|0|x|
# |x|x|x|0|0|0|
#
def rule_2(size, index):
    assert size > 1, 'size too small'

    if size < 3:
        return []
    
    rows = []
    cols = []

    # Row index rules
    for i in range(index * size, index * size + size - 3 + 1):
        row = []
        for j in range(0,  3):
            row.append(i + j + 1)

        rows.append(row)
        rows.append(list(map(lambda x: -x, row)))

    # Column index rules
    for i in range(0, size - 3 + 1):
        col = []
        for j in range(0,  3):
            col.append((i + j) * size + index + 1)

        cols.append(col)
        cols.append(list(map(lambda x: -x, col)))

    rows.extend(cols)
    return rows

def equal_row(table, fila1, fila2):
    for i in range(0, table.size()):
        cell1 = table.getCell(i, fila1)
        cell2 = table.getCell(i, fila2)
        if cell1 != '.' and cell2 != '.':
            if cell1 != cell2:
                return False
    return True

def equals(table, col1, col2):
    for i in range(0, table.size()):
        cell1 = table.getCell(col1, i)
        cell2 = table.getCell(col2, i)
        if cell1 != '.' and cell2 != '.':
            if cell1 != cell2:
                return False
    return True           

def proposicional_logic_row(size, count, fila1, fila2):
    sum1 = size * fila1 + 1
    sum2 = size * fila2 + 1
    clauses = []
    aux = []
    for i in range(1, size+1):
        count += 1
        clauses.append([-count, i + sum1, i + sum2])
        clauses.append([-count, -(i + sum1), -(i + sum2)])
        clauses.append([count, -(i + sum1), i + sum2])
        clauses.append([count, i + sum1, -(i + sum2)])
        aux.extend([count])
    clauses.append(aux)
    return clauses

def proposicional_logic_column(size, count, fila1, fila2):
    sum1 = fila1 + 1
    sum2 = fila2 + 1
    clauses = []
    aux = []
    for i in range(0, size):
        count += 1
        clauses.append([-count, i * size + sum1, i * size + sum2])
        clauses.append([-count, -(i * size + sum1), -(i * size + sum2)])
        clauses.append([count, -(i * size + sum1), i * size + sum2])
        clauses.append([count, i * size + sum1, -(i * size + sum2)])
        aux.extend([count])
    clauses.append(aux)
    return clauses

def propositional_logic(atm, num1, num2):
    clauses = []
    clauses.append([-atm, num1, num2])
    clauses.append([-atm, -num1, -num2])
    clauses.append([atm, -num1, num2])
    clauses.append([atm, num1, -num2])
    return clauses


def rule_3(table):
    size = table.size()
    distintRow = False
    distintCol = False
    count = size * size
    countRow = size * size
    countCol = size * size + size
    clauses = []
    rows = []
    cols = []
    for k in range(0, size - 1):
        for i in range(k + 1, size):
            for j in range(0, size):
                if not distintRow:
                    if not equals(table, table.getCell(j, k), table.getCell(j, i)):
                        #Borrar cosas demas y restar contador
                        distintRow = True
                        countRow -= j                        
                        count -= j
                        rows = []
                    else:
                        countRow += 1
                        count += 1
                        rows.extend(propositional_logic(count, j + size * k + 1, j + size * i + 1))

                if not distintCol: 
                    if not equals(table, table.getCell(k, j), table.getCell(i, j)):
                        #Borrar cosas demas y restar contador
                        distintCol = True   
                        countCol -= j
                        count -= j
                        cols = []
                    else:      
                        countCol += 1
                        count += 1                  
                        cols.extend(propositional_logic(count, j * size + k + 1, j * size + i + 1))
                #Poner false sumar contadores añadir clausulas
            clauses.extend(rows)
            clauses.extend(cols)
            if distintRow:
                distintRow = False
            else:
                countRow += size
            if distintCol:
                distintCol = False
            else:
                countCol += size

    return count, clauses

def rule_3_without(table):
    size = table.size()
    count = size * size
    clauses = []
    for k in range(0, size - 1):
        for i in range(k + 1, size):
            for j in range(0, size):
                count += 1
                clauses.extend(propositional_logic(count, j + size * k + 1, j + size * i + 1))
                count += 1
                clauses.extend(propositional_logic(count, j * size + k + 1, j * size + i + 1))
    return count, clauses
"""
def rule_3(table):
    size = table.size()
    count = size * size + 1
    clauses = []
    for k in range(0, size - 1):
        for i in range(k + 1, size):
            if equal_row(table, k, i):
                clauses.extend(proposicional_logic_row(size, count, k, i))
                count += size
            if equal_column(table, k, i):
                clauses.extend(proposicional_logic_column(size, count, k, i))
                count += size
    return clauses"""
#
# Main
#

t = Table.from_text(20,
    '........1.1..1.....1'
    '......0.....0....0.1'
    '...............01...'
    '.0..1.1.0.0.........'
    '1.0......1....0..0..'
    '...0..0........1..1.'
    '..00..0.0..00......0'
    '.......1...0.....0..'
    '10.1.11......00.....'
    '...........0..00.1.0'
    '.......0.......0..0.'
    '..0.1...0.......1...'
    '....11.....0.0......'
    '...1.1...00.1.1.....'
    '..1.............1.00'
    '...1..1..0..00.....0'
    '.....1...0......1...'
    '0.1...............11'
    '...1.....1..11...0..'
    '..11..11.....1.....1'
)
"""
t = Table.from_text(6,
    '.1....'
    '.....0'
    '..0..0'
    '1..1..'
    '....1.'
    '.....0'
)
"""


t = Table.from_file('sample.txt')


print(t)
print('')

size = t.size()
rules = []

# Initial state rule
rules.extend(rule_table(t))

# The three conditions rules
for i in range(0, size):
    rules.extend(rule_2(size, i))
    rules.extend(rule_1(size, i))
variable_count, clauses = rule_3_without(t)
rules.extend(clauses)
print("Fin")


"""
rules.extend(rule_table(Table.from_text(6, 
'100110'
'011001'
'010011'
'101100'
'110010'
'001101')))
"""

solutions, result = Clasp.resolve(
    variable_count, # Number of variables
    rules,
    max_solutions=0
)

for i in range(0, len(solutions)):
    print('Test solution {}'.format(i + 1))
    print(Table.from_values(solutions[i][0: size * size]))
    print('')