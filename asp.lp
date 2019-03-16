#show x/3.
values(white;black).
rows(1..size).
cols(1..size).

hint(1, 2, white).
hint(1, 3, white).
hint(1, 8, white).
hint(2, 1, black).
hint(2, 5, black).
hint(2, 7, white).
hint(3, 4, white).
hint(4, 3, white).
hint(4, 7, white).
hint(4, 9, black).
hint(5, 5, white).
hint(5, 6, white).
hint(5, 9, black).
hint(7, 1, white).
hint(7, 3, white).
hint(7, 4, white).
hint(7, 7, black).
hint(8, 5, black).
hint(8, 8, white).
hint(9, 3, white).
hint(9, 7, black).
hint(9, 8, black).
hint(10, 7, black).

% Genera x(X, Y, white) o x(X, Y, black) y forzamos a que elija uno
{ x(Row, Col, Val) : values(Val) } = 1 :- rows(Row), cols(Col).

x(Row, Col, Val) :- hint(Row, Col, Val).

% Rule 1
% Ejemplo: Genera x(Row, 1, black) o x(Row, 2, black) o x(Row, 3, black) o x(Row, 4, black) y forzamos a que elija 2
{ x(Row, Col, black) : cols(Col) } = size / 2 :- rows(Row).
{ x(Row, Col, black) : rows(Row) } = size / 2 :- cols(Col).

% Rule 2
% No puede haber tres filas seguidas del mismo color
% No puede haber tres columnas seguidas del mismo color
:- x(Row1, Col, Val), x(Row2, Col, Val), x(Row3, Col, Val), Row2 == Row1 + 1, Row3 == Row2 + 1.
:- x(Row, Col1, Val), x(Row, Col2, Val), x(Row, Col3, Val), Col2 == Col1 + 1, Col3 == Col2 + 1.

% Rule 3
% No puede haber una fila que no sea distinta a todas las demas, se deben diferenciar en al menos una columna
% No puede haber una columna que no sea distinta a todas las demas, se deben diferenciar en al menos una fila
distint_row(Row1, Row2, Col) :- x(Row1, Col, Val1), x(Row2, Col, Val2), Row1 != Row2, Val1 != Val2.
distint_col(Col1, Col2, Row) :- x(Row, Col1, Val1), x(Row, Col2, Val2), Col1 != Col2, Val1 != Val2.

:- rows(Row1), rows(Row2), Row1 != Row2, { distint_row(Row1, Row2, Col) : cols(Col) } = 0.
:- cols(Col1), cols(Col2), Col1 != Col2, { distint_col(Col1, Col2, Row) : rows(Row) } = 0.
