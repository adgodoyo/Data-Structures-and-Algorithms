from sys import stdin
def maximum_gold(capacity, weights):
    n = len(weights)
    # Creamos una tabla DP con dimensiones (n+1) x (capacity+1)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    # Llenamos la tabla DP
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            dp[i][w] = dp[i - 1][w]  # No tomar el peso actual
            if weights[i - 1] <= w:  # Si podemos tomar el peso actual
                dp[i][w] = max(dp[i][w], dp[i - 1][w - weights[i - 1]] + weights[i - 1])

    return dp[n][capacity]

# Ejemplo de uso
if __name__ == '__main__':
    import sys
    input_capacity, n, *input_weights = list(map(int, sys.stdin.read().split()))
    assert len(input_weights) == n

    print(maximum_gold(input_capacity, input_weights))
