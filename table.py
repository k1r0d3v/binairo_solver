import math

class Table:
    def __init__(self):
        self.__size = 0
        self.__date = None

    def size(self):
        return self.__size

    def data(self):
        return self.__data
    
    def get_cell(self, x, y):
        assert x < self.__size and y < self.__size, 'Index overflow'
        return self.__data[y * self.__size + x]

    def set_cell(self, x, y, value):
        assert x < self.__size and y < self.__size, 'Index overflow'
        assert len(value) == 1, 'Expected char value'
        assert value == '.' or value == '0' or value == '1', 'Invalid value, accepted values are: ".", "0", "1"'

        index = y * self.__size + x
        old = self.__data[index]
        self.__data[index] = value
        return old

    def get_row(self, y):
        assert y < self.__size, 'Index overflow'
        row = y * self.__size
        return self.__data[row:row + self.__size]

    def get_col(self, x):
        assert x < self.__size, 'Index overflow'

        col = []
        for i in range(0, self.__size):
            col.append(self.get_cell(x, i))
        return col

    def to_asp(self, name='hint', values=['white', 'black']):
        str = '#const size={}.\n'.format(self.__size)
        for i in range(0, self.__size):
            for j in range(0, self.__size):
                if self.__data[i * self.__size + j] == '.':
                    continue
                value = values[0]
                if self.__data[i * self.__size + j] == '1':
                    value = values[1]
                str += '{}({}, {}, {}).\n'.format(name, i + 1, j + 1, value)
        return str

    def __str__(self):
        str = ''
        for i in range(0, self.__size * self.__size):
            if (i != 0 and i % self.__size == 0):
                str += '\n'
            str += self.__data[i]
        return str

    # @param values:
    #   Negative values are white and
    #   positive values are black
    #
    #   white = 0 with values < 0
    #   black = 1 with values > 0
    #   
    #   The table's size is taken from the root square of values length,
    #   this is because the table is supposed to be an square
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
    def from_asp(size, text, name='x', values=['white', 'black']):
        t = Table()
        t.__size = size
        t.__data = ['.'] * size * size

        elements = text.split(' ')

        # ex. x(1, 2, black) -> x(
        entryStart = '{}('.format(name)

        for i in elements:
            entryIndex = i.find(entryStart)
            if entryIndex < 0:
                print('Warning: skipping element: {}'.format(i))
                continue
            
            i = i[entryIndex + len(entryStart):]
            i = i.replace('(', '')
            i = i.replace(')', '')
            
            a, b, c = i.split(',')

            index = (int(a) - 1) * size + (int(b) - 1)
            if index >= len(t.__data):
                print('Warning: Skipping index out of range ({}, {}, {})'.format(a, b, c))
                continue
            if t.__data[index] != '.':
                print('Warning: Overridded value ({}, {}, {})'.format(a, b, c))

            if c == values[0]:
                c = '0'
            elif c == values[1]:
                c = '1'        
            else:
                print('Warning: Unknown symbol: {}'.format(c))
            t.__data[index] = c
        return t

    # @param method: can be Table.from_asp or Table.from_text
    @staticmethod
    def from_file(filename, method):
        
        with open(filename, 'r') as file:
            size = int(file.readline())
            return method(size, file.read())
        raise Exception()