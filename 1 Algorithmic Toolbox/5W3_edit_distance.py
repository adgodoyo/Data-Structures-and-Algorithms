def edit_distance(first_string, second_string):
    n = len(first_string)
    m = len(second_string)

    # Crear una matriz para almacenar las distancias de edición
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    # Inicializar la primera fila y columna
    for i in range(n + 1):
        dp[i][0] = i  # Costo de eliminar todos los caracteres de first_string
    for j in range(m + 1):
        dp[0][j] = j  # Costo de insertar todos los caracteres de second_string

    # Llenar la matriz usando programación dinámica
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            insertion = dp[i][j - 1] + 1
            deletion = dp[i - 1][j] + 1
            substitution = dp[i - 1][j - 1] + (0 if first_string[i - 1] == second_string[j - 1] else 1)

            dp[i][j] = min(insertion, deletion, substitution)

    # La distancia de edición mínima está en dp[n][m]
    return dp[n][m]


if __name__ == "__main__":
    print(edit_distance(input(), input()))
