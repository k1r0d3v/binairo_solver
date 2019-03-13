#show foo/3.

#const size=8.
colors(white;black).
values(1..size).

table(1, 6, white).
table(1, 8, white).
table(2, 3, black).
table(2, 5, black).
table(2, 7, white).
table(3, 1, black).
table(3, 5, white).
table(4, 1, black).
table(4, 4, black).
table(5, 4, black).
table(5, 7, black).
table(6, 2, black).
table(6, 5, white).
table(6, 8, white).
table(7, 4, white).
table(7, 5, white).
table(8, 1, white).

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