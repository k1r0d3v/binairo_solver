import sys
import math

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
                str += 'table({}, {}, {}).\n'.format( i + 1, j + 1, value)
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



t = Table.from_file(sys.argv[1])
print(t.toAsp())