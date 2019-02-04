#!/bin/python3

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
        return self.__data[x * self.__size + y]

    def setCell(self, x, y, value):
        assert x < self.__size and y < self.__size, 'Index overflow'
        assert len(value) == 1, 'Expected char value'

        index = x * self.__size + y
        old = self.__data[index]
        self.__data[index] = value
        return old

    def __str__(self):
        str = ''
        for i in range(0, self.__size * self.__size):
            if (i != 0 and i % self.__size == 0):
                str += '\n'
            str += self.__data[i]
        return str

t = Table('sample.txt')
t.getCell(5, 0)
t.setCell(1, 1, '*')

print(t)
print(t.data())