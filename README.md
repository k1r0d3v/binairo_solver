# [Binairo puzzle](http://www.dc.fi.udc.es/~cabalar/kr/current/ex1.html) solver

## Prerequisitos
* Version de python >= 3.5
* Los ejecutables clasp y clingo deben de estar en el PATH del sistema

## SAT
#### Ejemplo de uso
```
$ binairo
Usage: binairo <filename>

$ binairo samples/3_8x8.txt
Size: 8
....0...
.1....1.
1.1..11.
.1......
......00
.....1..
...1....
0..1....

Solution: 1
11010100
01001011
10100110
01011001
10101100
01100110
10011001
00110011

Result: SATISFIABLE
Not passed rule 1: 0
Not passed rule 2: 0
Not passed rule 3: 0
```
	
## ASP
Archivo de reglas: `binairo.lp`
#### Ejecutable de utilidad
Se proporciona ademas un programa para convertir tablas a reglas asp
y de igual manera de reglas asp a una tabla, y por último ofrece la posibilidad de ejecutar `clingo` con varios archivos de reglas y mostrar los resultados como tablas.

#### Ejemplos de uso
```
$ asp_tester 
Usage: asp_helper (--table_to_asp <filename>) | (--table_from_asp <size> <text>) | (--execute_asp <max_solutions> <filename> [<filename>...])
```

##### Genera las reglas de pistas iniciales para ASP junto con la constante #const size de una tabla en formato texto
```
$ asp_tester --table_to_asp samples/3_8x8.txt
#const size=8.
hint(1, 5, white).
hint(2, 2, black).
hint(2, 7, black).
hint(3, 1, black).
hint(3, 3, black).
hint(3, 6, black).
hint(3, 7, black).
hint(4, 2, black).
hint(5, 7, white).
hint(5, 8, white).
hint(6, 6, black).
hint(7, 4, black).
hint(8, 1, white).
hint(8, 4, black).

```

##### Guardar la salida de pistas iniciales
```
$ asp_tester --table_to_asp samples/3_8x8.txt > hints.lp
```

##### Uso con clingo
```
$ clingo 0 binairo.lp hints.lp
clingo version 5.3.0
Reading from binairo.lp ...
Solving...
Answer: 1
x(8,1,white) x(1,5,white) x(5,7,white) x(5,8,white) x(3,1,black) x(2,2,black) x(4,2,black) x(3,3,black) x(7,4,black) x(8,4,black) x(3,6,black) x(6,6,black) x(2,7,black) x(3,7,black) x(1,2,black) x(1,4,black) x(1,6,black) x(1,1,black) x(1,3,white) x(1,7,white) x(1,8,white) x(2,1,white) x(2,5,black) x(2,8,black) x(2,3,white) x(2,4,white) x(2,6,white) x(3,2,white) x(3,4,white) x(3,5,white) x(3,8,white) x(4,1,white) x(4,4,black) x(4,5,black) x(4,8,black) x(4,3,white) x(4,6,white) x(4,7,white) x(5,3,black) x(5,5,black) x(5,6,black) x(5,1,black) x(5,2,white) x(5,4,white) x(6,1,white) x(6,2,black) x(6,3,black) x(6,7,black) x(6,4,white) x(6,5,white) x(6,8,white) x(7,5,black) x(7,8,black) x(7,1,black) x(7,2,white) x(7,3,white) x(7,6,white) x(7,7,white) x(8,3,black) x(8,7,black) x(8,8,black) x(8,2,white) x(8,5,white) x(8,6,white)
SATISFIABLE

Models       : 1
Calls        : 1
Time         : 0.029s (Solving: 0.00s 1st Model: 0.00s Unsat: 0.00s)
CPU Time     : 0.029s
```

##### Muestra la tabla desde un conjunto de reglas
```
$ asp_tester --table_from_asp 8 "x(8,1,white) x(1,5,white) x(5,7,white) x(5,8,white) x(3,1,black) x(2,2,black) x(4,2,black) x(3,3,black) x(7,4,black) x(8,4,black) x(3,6,black) x(6,6,black) x(2,7,black) x(3,7,black) x(1,2,black) x(1,4,black) x(1,6,black) x(1,1,black) x(1,3,white) x(1,7,white) x(1,8,white) x(2,1,white) x(2,5,black) x(2,8,black) x(2,3,white) x(2,4,white) x(2,6,white) x(3,2,white) x(3,4,white) x(3,5,white) x(3,8,white) x(4,1,white) x(4,4,black) x(4,5,black) x(4,8,black) x(4,3,white) x(4,6,white) x(4,7,white) x(5,3,black) x(5,5,black) x(5,6,black) x(5,1,black) x(5,2,white) x(5,4,white) x(6,1,white) x(6,2,black) x(6,3,black) x(6,7,black) x(6,4,white) x(6,5,white) x(6,8,white) x(7,5,black) x(7,8,black) x(7,1,black) x(7,2,white) x(7,3,white) x(7,6,white) x(7,7,white) x(8,3,black) x(8,7,black) x(8,8,black) x(8,2,white) x(8,5,white) x(8,6,white)"
11010100
01001011
10100110
01011001
10101100
01100110
10011001
00110011
```

##### Ejecuta un conjunto de archivos de reglas en clingo y testea la salida comprobando cuantos modelos no cumplen las reglas binairo
Ejecuta en clingo `binairo.lp` y `hints.lp`

> Al menos unos de los archivos de entrada debe contener la constante size.
Si usas la opción --table_to_asp no tendrás problemas por que ya la genera por ti.

```
$ asp_tester --execute_asp 0 binairo.lp hints.lp
11010100
01001011
10100110
01011001
10101100
01100110
10011001
00110011

Result: SATISFIABLE
Not passed rule 1: 0
Not passed rule 2: 0
Not passed rule 3: 0
```


## Ejemplos
La carpeta samples posee un conjunto de ejemplos de tablas obtenidas automáticamente de la propia página de binairo con el script `generate_samples.py`. 
> generate_samples.py hace uso de librerias no estandar