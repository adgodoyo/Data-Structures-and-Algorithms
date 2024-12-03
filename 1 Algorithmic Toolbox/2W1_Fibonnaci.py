def numero_fibonacci(n):
    if n <= 1:
        return n
    anterior = 0
    actual = 1
    for _ in range(2, n + 1):
        siguiente = anterior + actual
        anterior = actual
        actual = siguiente
    return actual

if __name__ == '__main__':
    entrada = int(input())
    print(numero_fibonacci(entrada))
