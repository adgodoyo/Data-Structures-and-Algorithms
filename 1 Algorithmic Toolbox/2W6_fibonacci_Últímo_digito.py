def obtener_periodo_pisano(m):
    anterior, actual = 0, 1
    for i in range(0, m * m):
        anterior, actual = actual, (anterior + actual) % m
        if anterior == 0 and actual == 1:
            return i + 1

def fibonacci_mod(n, m):
    periodo_pisano = obtener_periodo_pisano(m)
    n = n % periodo_pisano
    if n <= 1:
        return n

    anterior, actual = 0, 1
    for _ in range(n - 1):
        anterior, actual = actual, (anterior + actual) % m

    return actual

def suma_fibonacci(n):
    if n <= 1:
        return n
    ultimo_digito = (fibonacci_mod(n + 2, 10) - 1) % 10
    return ultimo_digito

if __name__ == '__main__':
    n = int(input())
    print(suma_fibonacci(n))
