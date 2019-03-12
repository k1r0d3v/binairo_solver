#const size=4.
colors(white;black).
values(1..size).

table(1, 1, black).
table(1, 3, black).
table(2, 2, black).
table(2, 3, white).
table(3, 3, white).
table(3, 4, white).
table(4, 1, white).
table(4, 3, black).


size * size { table(X, Y, N) : values(X), values(Y), colors(N) } size * size.
 :- table(X, Y, A), table(X, Y, B), A != B.
% :- table(X, Y, Z), table(X, Y + 1, Z), table(X, Y + 2, Z).
:- #count{C: table(X, 1, C)} = S, S != size / 2.
:- #count{C: table(X, 2, C)} = S, S != size / 2.
:- #count{C: table(X, 3, C)} = S, S != size / 2.
:- #count{C: table(X, 4, C)} = S, S != size / 2.