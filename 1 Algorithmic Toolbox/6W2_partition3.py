from sys import stdin


def partition3(values):
    total_sum = sum(values)
    n = len(values)

    # Si la suma total no es divisible entre 3, no es posible dividir en tres subconjuntos
    if total_sum % 3 != 0:
        return 0

    target = total_sum // 3

    # Creamos una tabla DP donde dp[i][j][k] indica si es posible formar las sumas `j` y `k`
    dp = [[[False] * (target + 1) for _ in range(target + 1)] for _ in range(n + 1)]
    dp[0][0][0] = True  # Caso base: se puede formar 0 con 0 elementos

    for i in range(1, n + 1):
        for j in range(target + 1):
            for k in range(target + 1):
                # Caso 1: no incluir el elemento actual
                dp[i][j][k] = dp[i - 1][j][k]

                # Caso 2: incluir el elemento en el primer subconjunto
                if j >= values[i - 1]:
                    dp[i][j][k] |= dp[i - 1][j - values[i - 1]][k]

                # Caso 3: incluir el elemento en el segundo subconjunto
                if k >= values[i - 1]:
                    dp[i][j][k] |= dp[i - 1][j][k - values[i - 1]]

    # Verificamos si es posible formar tres subconjuntos con la suma objetivo
    return 1 if dp[n][target][target] else 0


if __name__ == '__main__':
    import sys
    input_n, *input_values = list(map(int, sys.stdin.read().split()))
    assert input_n == len(input_values)
    print(partition3(input_values))

