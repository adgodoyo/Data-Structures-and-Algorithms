# Uses python3
import sys
import heapq
from math import sqrt


def distancia_minima(x, y):
    resultado = 0
    n = len(x)

    costos = [float("inf")] * n
    costos[0] = 0

    visitados = [False] * n

    pq = []  # cola de prioridad
    inicio = (0, 0)  # (prioridad, ID)
    heapq.heappush(pq, inicio)

    while pq:
        w, actual = heapq.heappop(pq)

        if not visitados[actual]:
            visitados[actual] = True
            resultado += w

            for i in range(n):
                if not visitados[i]:
                    distancia = sqrt((x[i] - x[actual])**2 + (y[i] - y[actual])**2)
                    if distancia < costos[i]:
                        costos[i] = distancia
                        heapq.heappush(pq, (distancia, i))

    return resultado


def ejecutar_algoritmo():
    datos = list(map(int, sys.stdin.read().split()))
    n = datos[0]
    x = datos[1::2]
    y = datos[2::2]
    print("{0:.9f}".format(distancia_minima(x, y)))

if __name__ == "__main__":
    ejecutar_algoritmo()
