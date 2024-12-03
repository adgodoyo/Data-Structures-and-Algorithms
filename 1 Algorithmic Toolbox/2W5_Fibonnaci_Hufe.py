def obtener_periodo_pisano(m):
    anterior, actual = 0, 1
    for i in range(0, m * m):
        anterior, actual = actual, (anterior + actual) % m
        if anterior == 0 and actual == 1:
            return i + 1

def fibonacci_huge(n, m):
    periodo_pisano = obtener_periodo_pisano(m)
    n = n % periodo_pisano
    if n <= 1:
        return n
    
    anterior, actual = 0, 1
    for _ in range(n - 1):
        anterior, actual = actual, (anterior + actual) % m
    
    return actual

if __name__ == '__main__':
    n, m = map(int, input().split())
    print(fibonacci_huge(n, m))

