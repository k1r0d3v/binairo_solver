def proposicional_logic_row(size, count, fila1, fila2):
    sum1 = size * fila1 + 1
    sum2 = size * fila2 + 1
    clauses = []
    aux = []
    for i in range(0, size):
        count += 1
        clauses.append([-count, i + sum1, i + sum2])
        clauses.append([-count, -(i + sum1), -(i + sum2)])
        clauses.append([count, -(i + sum1), -(i + sum2)])
        clauses.append([count, i + sum1, -(i + sum2)])
        aux.extend([count])
    clauses.append(aux)
    return clauses

count = 36
proposicional_logic_row(6, count, 0, 2)
print(count)