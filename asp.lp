#show foo/3.

#const size=20.
colors(white;black).
values(1..size).

table(1, 6, black).
table(1, 9, black).
table(1, 10, white).
table(1, 12, white).
table(1, 16, black).
table(2, 1, black).
table(2, 5, black).
table(2, 11, white).
table(2, 12, white).
table(2, 18, black).
table(2, 20, white).
table(3, 3, white).
table(3, 8, black).
table(3, 9, black).
table(3, 14, black).
table(3, 19, white).
table(3, 20, white).
table(4, 1, white).
table(4, 3, white).
table(4, 9, white).
table(4, 15, white).
table(4, 17, white).
table(5, 4, black).
table(5, 11, white).
table(5, 17, white).
table(5, 18, black).
table(6, 1, black).
table(6, 2, black).
table(6, 12, black).
table(6, 13, black).
table(6, 18, black).
table(7, 4, white).
table(7, 9, black).
table(7, 16, black).
table(7, 20, white).
table(8, 2, white).
table(8, 4, white).
table(8, 7, black).
table(8, 10, white).
table(8, 13, black).
table(8, 14, black).
table(9, 3, black).
table(9, 7, black).
table(9, 9, black).
table(10, 4, white).
table(10, 6, white).
table(10, 13, black).
table(10, 16, white).
table(10, 18, black).
table(10, 20, white).
table(11, 10, black).
table(11, 12, white).
table(11, 20, white).
table(12, 4, black).
table(12, 6, white).
table(12, 7, white).
table(12, 9, black).
table(12, 11, black).
table(12, 14, black).
table(13, 1, black).
table(13, 3, black).
table(13, 6, black).
table(13, 15, white).
table(13, 17, black).
table(14, 12, black).
table(14, 14, black).
table(14, 15, white).
table(14, 18, black).
table(15, 3, black).
table(15, 9, white).
table(15, 16, black).
table(15, 18, black).
table(15, 20, white).
table(16, 5, white).
table(16, 6, white).
table(17, 5, white).
table(17, 10, black).
table(18, 9, white).
table(18, 11, white).
table(18, 14, black).
table(18, 17, white).
table(19, 2, white).
table(19, 4, white).
table(19, 9, white).
table(19, 14, black).
table(19, 19, black).
table(19, 20, black).
table(20, 4, white).
table(20, 5, black).
table(20, 17, white).
table(20, 20, black).

size * size { foo(X, Y, Z) : values(X), values(Y), colors(Z) } size * size.

% Force initial table
foo(X, Y, Z) :- table(X, Y, Z).

% Do not repeat indices
:- foo(X, Y, Z), foo(X, Y, C), Z!=C.

% Rule 1
:- foo(X, B, C), #count {Y: foo(X, Y, black)} = S, S!=size/2.
:- foo(A, Y, C), #count {X: foo(X, Y, black)} = S, S!=size/2.

% Rule 2
:- foo(X, Y, Z), foo(X, Y + 1, Z), foo(X, Y + 2, Z).
:- foo(X, Y, Z), foo(X + 1, Y, Z), foo(X + 2, Y, Z).

% Rule 3
%
%row_equals(X1, X2) 
:- foo(X1, Y1, Z2), foo(X2, Y2, Z2), X1 != X2, #count { Y: foo(X1, Y, C1), foo(X2, Y, C2), C1=C2 } = S, S = size.
%
%col_equals(Y1, Y2) 
:- foo(X1, Y1, Z2), foo(X2, Y2, Z2), Y1 != Y2, #count { X: foo(X, Y1, C1), foo(X, Y2, C2), C1=C2 } = S, S = size.

