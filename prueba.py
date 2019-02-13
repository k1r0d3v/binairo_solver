def proposicional_logic(size, count, fila1, fila2):
    sum1 = fila1 + 1
    sum2 = fila2 + 1
    clauses = []
    aux = []
    for i in range(0, size):
        count += 1
        clauses.append([-count, i * size + sum1, i * size + sum2])
        clauses.append([-count, -(i * size + sum1), -(i * size + sum2)])
        clauses.append([count, -(i * size + sum1), -(i * size + sum2)])
        clauses.append([count, i * size + sum1, -(i * size + sum2)])
        aux.extend([count])
    clauses.append(aux)
    return clauses

count = 36
proposicional_logic(6, count, 0, 2)
print(count)