def evaluate(a, b, op):
    if op == '+':
        return a + b
    elif op == '-':
        return a - b
    elif op == '*':
        return a * b
    else:
        raise ValueError("Invalid operator")

def min_and_max(i, j, ops, m, M):
    minimum = float('inf')
    maximum = float('-inf')
    for k in range(i, j):
        op = ops[k]
        a = evaluate(M[i][k], M[k+1][j], op)
        b = evaluate(M[i][k], m[k+1][j], op)
        c = evaluate(m[i][k], M[k+1][j], op)
        d = evaluate(m[i][k], m[k+1][j], op)
        minimum = min(minimum, a, b, c, d)
        maximum = max(maximum, a, b, c, d)
    return minimum, maximum

def maximum_value(dataset):
    digits = list(map(int, dataset[0::2]))
    ops = list(dataset[1::2])
    n = len(digits)

    # Tablas para almacenar los valores mínimos y máximos
    m = [[0] * n for _ in range(n)]
    M = [[0] * n for _ in range(n)]

    for i in range(n):
        m[i][i] = digits[i]
        M[i][i] = digits[i]

    for s in range(1, n):  # s es el tamaño de la subexpresión
        for i in range(n - s):
            j = i + s
            m[i][j], M[i][j] = min_and_max(i, j, ops, m, M)

    return M[0][n - 1]

if __name__ == "__main__":
    print(maximum_value(input()))
