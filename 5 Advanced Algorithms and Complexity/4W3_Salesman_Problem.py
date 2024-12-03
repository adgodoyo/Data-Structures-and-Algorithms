# python3
from itertools import permutations, combinations
from collections import defaultdict
import random
from time import sleep


class Viajante:

    INF = 10 ** 12

    def __init__(self, grafo):
        self.grafo = grafo
        self.n = len(self.grafo)

    def camino_optimo_dp(self):
        longitud_camino = dict()
        longitud_camino[(1, 0)] = 0

        tamanio_conjunto_k = defaultdict(list)
        for k in range(1, 2**self.n):
            k_bin = format(k, "b")

            if k_bin[-1] != "1":
                continue

            count_one = 0
            for i in k_bin:
                if i == "1":
                    count_one += 1
            tamanio_conjunto_k[count_one].append(k)

        for k in tamanio_conjunto_k[2]:
            i = 0
            k_bin = format(k, "b")
            for j, c in enumerate(reversed(k_bin[:-1])):
                if c == "1":
                    i = j + 1
                    break

            longitud_camino[(k, i)] = self.grafo[0][i]

        for tamanio_conjunto in range(3, self.n + 1):
            for k in tamanio_conjunto_k[tamanio_conjunto]:
                longitud_camino[(k, 0)] = Viajante.INF
                longitud_minima = Viajante.INF

                k_bin = format(k, "b")

                for i, c1 in enumerate(reversed(k_bin)):
                    if (i == 0) or (c1 == "0"):
                        continue

                    longitud_camino[(k, i)] = Viajante.INF

                    for j, c2 in enumerate(reversed(k_bin)):
                        if (j == i) or (j == 0) or (c2 == "0"):
                            continue

                        k_sin_i = k ^ (1 << i)
                        nueva_longitud = longitud_camino[(k_sin_i, j)] + self.grafo[i][j]
                        if nueva_longitud < longitud_camino[(k, i)]:
                            longitud_camino[(k, i)] = nueva_longitud

                            if nueva_longitud < longitud_minima:
                                longitud_minima = nueva_longitud

        longitud_total = Viajante.INF
        k = tamanio_conjunto_k[self.n][0]
        ultimo_i = None
        for i in range(1, self.n):
            nueva_longitud = longitud_camino[(k, i)] + self.grafo[i][0]
            if nueva_longitud < longitud_total:
                longitud_total = nueva_longitud
                ultimo_i = i

        if longitud_total == Viajante.INF:
            return -1, []

        camino = [1, ultimo_i + 1]
        k = tamanio_conjunto_k[self.n][0] ^ (1 << ultimo_i)
        longitud_actual = longitud_camino[(tamanio_conjunto_k[self.n][0], ultimo_i)]
        tamanio_actual = self.n - 1
        while k != 1:
            k_bin = format(k, "b")
            for i, c in enumerate(reversed(k_bin)):
                if (i == 0) or (c == "0"):
                    continue
                nueva_longitud = longitud_camino[(k, i)] + self.grafo[i][ultimo_i]
                if nueva_longitud == longitud_actual:
                    longitud_actual = longitud_camino[(k, i)]
                    k = k ^ (1 << i)
                    ultimo_i = i
                    camino.append(i + 1)
                    break
        camino.append(1)
        return longitud_total, camino

def algoritmo():
    n_vertices, n_aristas = map(int, input().split())
    grafo = [[Viajante.INF] * n_vertices for _ in range(n_vertices)]
    for _ in range(n_aristas):
        u_, v_, peso = map(int, input().split())
        u, v = u_ - 1, v_ - 1
        grafo[u][v] = grafo[v][u] = peso

    tsp = Viajante(grafo)
    longitud_camino, camino = tsp.camino_optimo_dp()

    print(longitud_camino)
    if longitud_camino == -1:
        return
    print(" ".join(map(str, camino[:-1])))


if __name__ == "__main__":
    algoritmo()
