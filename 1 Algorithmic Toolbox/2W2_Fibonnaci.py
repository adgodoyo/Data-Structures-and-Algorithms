def ultimo_digito_fibonacci(n):
    if n <= 1:
        return n
    
    anterior = 0
    actual = 1

    for _ in range(n - 1):
        anterior, actual = actual, (anterior + actual) % 10

    return actual

if __name__ == '__main__':
    entrada = int(input())
    print(ultimo_digito_fibonacci(entrada))
