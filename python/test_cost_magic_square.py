#!/bin/python3

import math
import os
import random
import re
import sys
import itertools

#
# Complete the 'formingMagicSquare' function below.
#
# The function is expected to return an INTEGER.
# The function accepts 2D_INTEGER_ARRAY s as parameter.
#

def formingMagicSquare(s):
    magic_square = sum(magic_square, [])
    # Compara cada uno de los cuadros magicos con el cuadro magico
    # dado como entrada. 
    # De los cuadros magicos en comparacion hace un zip para extraer pares de tuplas,
    # compara los valores de cada tupla, ej: (1,2)=1; (3,3)=0 . Se asigna 1 cuando no
    # coincide y 0 si coincide, la sumatoria de todos los 1 o 0 nos dejara el valor
    # de coincidencia, el menor de todos sera devuelto como el cuadro magico cercano
    closetst_ms = min(all_magic_squares_3_x_3(), 
                key=(lambda x: sum(i!=j for i, j in zip(magic_square, x))))
    # Extrae la diferencia entre los valores de los dos cuadros
    return sum([abs(i-j) for i, j in zip(magic_square, closetst_ms)])

def all_magic_squares_3_x_3():
    # Indices de un cuadro magico 3x3
    all_index = [# filas
                [0, 1, 2], 
                [3, 4, 5], 
                [6, 7, 8], 
                # columnas
                [0, 3, 6], 
                [1, 4, 7], 
                [2, 5, 8], 
                # diagonales
                [0, 4, 8], 
                [2, 4, 6]]

    # Obtiene todas las permutaciones de 1-9
    for p in itertools.permutations(range(1, 10)):
        # verifica cual de dichas permutaciones devuelve 15 en todas las posibles sumas
        # dados los indices de todas las filas, columnas y diagonales
        if all(sum(p[i] for i in index_row) == 15 for index_row in all_index):
            yield list(p)
            
if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    s = []

    for _ in range(3):
        s.append(list(map(int, input().rstrip().split())))

    result = formingMagicSquare(s)

    fptr.write(str(result) + '\n')

    fptr.close()
