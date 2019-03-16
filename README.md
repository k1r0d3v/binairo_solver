#[Binairo puzzle](http://www.dc.fi.udc.es/~cabalar/kr/current/ex1.html) solver

## Prerequisitos
* Version de python >= 3.5
* Los ejecutables clasp y clingo deben de estar en el PATH del sistema

## SAT
#### Ejemplo de uso
```
# Usage: binairo <table>
# where table is a text document with the expected format <size>\n<values>

./binairo samples/3_8x8.txt
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
# Usage: asp_helper (--table_to_asp <filename>) | (--table_from_asp <size> <text>) | (--execute_asp <size> <max_solutions> <filename> [<filename>...])


```


## Ejemplos
La carpeta samples posee un conjunto de ejemplos de tablas obtenidas automáticamente de la propia página de binairo con el script `generate_samples.py`. 
> generate_samples.py hace uso de librerias no estandar