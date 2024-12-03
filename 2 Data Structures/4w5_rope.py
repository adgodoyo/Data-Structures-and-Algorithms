import sys

if __name__ == "__main__":
    cadena = sys.stdin.readline().strip()
    consultas = int(sys.stdin.readline())
    for _ in range(consultas):
        inicio, fin, posicion = map(int, sys.stdin.readline().strip().split())
        parte = cadena[inicio:fin+1]
        resto = cadena[:inicio] + cadena[fin+1:]
        cadena = resto[:posicion] + parte + resto[posicion:]
    print(cadena)