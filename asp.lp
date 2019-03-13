#show x/3.
%#show distint/2.
values(white;black).
rows(1..size).
cols(1..size).

hint(1, 1, black).
hint(1, 3, black).
hint(2, 2, black).
hint(2, 3, white).
hint(3, 3, white).
hint(3, 4, white).
hint(4, 1, white).
hint(4, 3, black).

1 { x(Row, Col, Val) : values(Val) } 1 :- rows(Row), cols(Col).

x(Row, Col, Val) :- hint(Row, Col, Val).

size / 2 { x(Row, Col, black) : cols(Col) } size / 2 :- rows(Row).
size / 2 { x(Row, Col, black) : rows(Row) } size / 2 :- cols(Col).

:- x(Row1, Col, Val), x(Row2, Col, Val), x(Row3, Col, Val), Row2 == Row1 + 1, Row3 == Row2 + 1.
:- x(Row, Col1, Val), x(Row, Col2, Val), x(Row, Col3, Val), Col2 == Col1 + 1, Col3 == Col2 + 1.


% Rule 3
%
%row_equals(X1, X2) 
%:- foo(X1, Y1, Z2), foo(X2, Y2, Z2), X1 != X2, #count { Y: foo(X1, Y, C1), foo(X2, Y, C2), C1=C2 } = S, S = size.
%
%col_equals(Y1, Y2) 
%:- foo(X1, Y1, Z2), foo(X2, Y2, Z2), Y1 != Y2, #count { X: foo(X, Y1, C1), foo(X, Y2, C2), C1=C2 } = S, S = size.
