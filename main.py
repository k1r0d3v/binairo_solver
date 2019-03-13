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

    def toAsp(self):
        str = ''
        for i in range(0, self.__size):
            for j in range(0, self.__size):
                if self.__data[i * self.__size + j] == '.':
                    continue
                value = 'white'
                if self.__data[i * self.__size + j] == '1':
                    value = 'black'
                str += 'table({}, {}, {}).'.format( i + 1, j + 1, value)
        return str

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


def rule_1_base(rows, row, cnt, size):
    if len(row) > 2:
        if row[-1] < 0 and row[-2] < 0 and row[-3] < 0:
            return        
        if row[-1] > 0 and row[-2] > 0 and row[-3] > 0:
            return
    
    if len(row) == size and cnt != 0:
        return

    if len(row) == size:
        rows.append(row)
        return

    if cnt != 0:               
        rule_1_base(rows, row + [1], cnt - 1, size)

    row.append(-1)
    rule_1_base(rows, row, cnt, size)

# TODO: Explain
#
# Cases not in permutations of
# |0|0|0|1|1|1|
#
def rule_1(size):
    cnt = size // 2
    rows = []

    # Base row generation
    base = []
    for i in range(0, cnt):
        rule_1_base(base, [], i, size)

    for i in base:        
        for w in range(0, size):
            # Generate rows base
            # Generate columns base
            row = []
            col = []
            for j, k in enumerate(i):
                row.append(i[j] * (j + 1 + w * size))
                col.append(k * (j * size + 1 + w))
            rows.append(row)                
            rows.append(col)
            
            row = row.copy()
            col = col.copy()
            for j in range(0, size):
                row[j] *= -1
                col[j] *= -1
            rows.append(row)
            rows.append(col)

    return rows


# TODO: Explain
#
# |0|0|0|x|x|x|
# |x|0|0|0|x|x|
# |x|x|0|0|0|x|
# |x|x|x|0|0|0|
def rule_2(size):
    assert size > 1, 'size too small'

    if size < 3:
        return []
    
    rows = []
    cols = []

    for index in range(0, size):
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

def equals(table, cell1, cell2):
    if cell1 != '.' and cell2 != '.':
            if cell1 != cell2:
                return False
    return True           

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
                        rows.extend(propositional_logic(countRow, j + size * k + 1, j + size * i + 1))

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
                        cols.extend(propositional_logic(countCol, j * size + k + 1, j * size + i + 1))
                #Poner false sumar contadores añadir clausulas
            clauses.extend(rows)
            clauses.extend(cols)
            if distintRow:
                distintRow = False
            else:
                clauses.append(list(range(countRow-size + 1, countRow + 1)))
                countRow += size
            if distintCol:
                distintCol = False
            else:
                clauses.append(list(range(countCol-size + 1, countCol + 1)))
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
            clauses.append(list(range(count-size * 2 + 1, count, 2)))
            clauses.append(list(range(count-size * 2 + 2, count, 2)))
               
    return count, clauses

def equals_row(n, a, b):
    for i in range(0, n):
        if a[i] != b[i]:
            return False
    return True

def test_rule_3(n, t):
    for i in range(0, t.size()):
        for j in range(0, t.size()):
            if i != j and equals_row(n, t.getRow(i), t.getRow(j)):
                raise Exception('Test rule 3 fail: {} {}'.format(i, j))
            if i != j and equals_row(n, t.getColumn(i), t.getColumn(j)):
                raise Exception('Test rule 3 fail: {} {}'.format(i, j))

if __name__ == "__main__":
    #
    # Main
    #
    #t = Table.from_file('samples/1_6x6.txt')
    #t = Table.from_file('samples/1_6x6.txt')
    #t = Table.from_file('samples/2_8x8.txt')
    #t = Table.from_file('samples/3_8x8.txt')
    #t = Table.from_file('samples/4_10x10.txt')
    #t = Table.from_file('samples/5_10x10.txt')
    #t = Table.from_file('samples/6_14x14.txt')
    #t = Table.from_file('samples/7_14x14.txt')
    t = Table.from_file('samples/8_20x20.txt')
    #t = Table.from_file('samples/9_20x20.txt')
    #t = Table.from_file('samples/10_24x24.txt')
    #t = Table.from_file('samples/11_30x30.txt')
    #t = Table.from_file('samples/12_34x34.txt')


    print('{}\n'.format(t))

    size = t.size()
    rules = []

    # Initial state rule
    rules.extend(rule_table(t))

    # The three conditions rules
    rules.extend(rule_1(size))
    rules.extend(rule_2(size))
    #variable_count, clauses = rule_3(t)
    variable_count, clauses = rule_3_without(t)
    rules.extend(clauses)

    solutions, result = Clasp.resolve(
        variable_count, # Number of variables
        rules,
        max_solutions=10
    )

    for i in range(0, len(solutions)):
        print('Test solution {}'.format(i + 1))
        t = Table.from_values(solutions[i][0: size * size])
        test_rule_3(size, t)
        zeros = [0] * size
        for j in range(0, size):
            zeros[j] = len(list(filter(lambda x: x == '0', t.getColumn(j))))

            row = t.getRow(j)
            print('{} - zeros: {}'.format(row, len(list(filter(lambda x: x == '0', row)))))
        
        print('Column zeros: {}'.format(zeros))