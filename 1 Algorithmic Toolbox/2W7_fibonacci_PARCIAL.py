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

def suma_parcial_fibonacci(desde, hasta):
    if hasta < desde:
        return 0

    suma_hasta = (fibonacci_mod(hasta + 2, 10) - 1) % 10
    suma_desde = (fibonacci_mod(desde + 1, 10) - 1) % 10

    resultado = (suma_hasta - suma_desde) % 10
    return resultado

if __name__ == '__main__':
    desde, hasta = map(int, input().split())
    print(suma_parcial_fibonacci(desde, hasta))
