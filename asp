#!/bin/python3
import sys
import math

class Table:
    def __init__(self):
        self.__size = 0
        self.__date = None

    def __str__(self):
        str = ''
        for i in range(0, self.__size * self.__size):
            if (i != 0 and i % self.__size == 0):
                str += '\n'
            str += self.__data[i]
        return str
    

    def toAsp(self):
        str = ''
        for i in range(0, self.__size):
            for j in range(0, self.__size):
                if self.__data[i * self.__size + j] == '.':
                    continue
                value = 'white'
                if self.__data[i * self.__size + j] == '1':
                    value = 'black'
                str += 'hint({}, {}, {}).\n'.format( i + 1, j + 1, value)
        return str

    @staticmethod
    def fromAsp(size, text):
        t = Table()
        t.__size = size
        t.__data = ['.'] * size * size

        elements = text.split(' ')
        if len(elements) != size * size:
            print('Expected {} entries, given {}'.format(size * size, len(elements)))
            exit(-1)
        
        for i in elements:
            i = i[i.find('('):]
            i = i.replace('(', '')
            i = i.replace(')', '')
            
            a, b, c = i.split(',')


            index = (int(a) - 1) * size + (int(b) - 1)
            if t.__data[index] != '.':
                print('Warning: Overridded value ({}, {}, {})'.format(a, b, c))

            if c == 'white':
                c = '0'
            else:
                c = '1'            
            t.__data[index] = c
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

def print_usage():
    print('USAGE: asp <table.txt | -p <size> <asp_result>>')
    print('    <asp_result> format: (x, y, <white | black>) ...')

if len(sys.argv) > 1 and sys.argv[1] == '-p':
    if len(sys.argv) != 4:
        print_usage()
    else:
        print(Table.fromAsp(int(sys.argv[2]), sys.argv[3]))
elif len(sys.argv) == 2:
    t = Table.from_file(sys.argv[1])
    print(t.toAsp())
else:
    print_usage()