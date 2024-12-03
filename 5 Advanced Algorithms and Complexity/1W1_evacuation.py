# python3
from copy import deepcopy
from collections import deque


class Arista:
    def __init__(self, inicio, fin, capacidad):
        self.inicio = inicio
        self.fin = fin
        self.capacidad = capacidad
        self.flujo = 0

    def __str__(self):
        return "Arista(inicio={}, fin={}, capacidad={}, flujo={})".format(
            self.inicio + 1, self.fin + 1, self.capacidad, self.flujo
        )

    def __repr__(self):
        return "\nArista(inicio={}, fin={}, capacidad={}, flujo={})".format(
            self.inicio + 1, self.fin + 1, self.capacidad, self.flujo
        )


class GrafoDeFlujo:
    def __init__(self, n):
        self.n = n
        self.aristas = []
        self.grafo = [[] for _ in range(n)]

    def agregar_arista(self, inicio, fin, capacidad):
        arista_directa = Arista(inicio, fin, capacidad)
        arista_reversa = Arista(fin, inicio, 0)
        self.grafo[inicio].append(len(self.aristas))
        self.aristas.append(arista_directa)
        self.grafo[fin].append(len(self.aristas))
        self.aristas.append(arista_reversa)

    def encontrar_camino_mas_corto(self, inicio, fin):
        padre = [None] * self.n
        procesados = [False] * self.n
        procesados[inicio] = True
        cola = deque([inicio])

        while cola:
            actual = cola.popleft()

            if actual == fin:
                break

            for id_arista in self.grafo[actual]:
                arista = self.aristas[id_arista]
                if not procesados[arista.fin] and arista.flujo > 0:
                    cola.append(arista.fin)
                    padre[arista.fin] = (id_arista, arista)
                    procesados[arista.fin] = True

        camino = []
        if padre[fin] is not None:
            nodo_actual = fin
            while nodo_actual != inicio:
                id_arista, arista = padre[nodo_actual]
                camino.append((id_arista, arista))
                nodo_actual = arista.inicio

            camino = camino[::-1]

        return camino

    def flujo_maximo(self, inicio, fin):
        grafo_residual = deepcopy(self)
        for i in range(len(grafo_residual.aristas) // 2):
            grafo_residual.aristas[i * 2].flujo = grafo_residual.aristas[i * 2].capacidad

        flujo = 0
        while True:
            camino = grafo_residual.encontrar_camino_mas_corto(inicio, fin)
            if not camino:
                break

            flujo_minimo = min(arista.flujo for _, arista in camino)

            for id_arista, _ in camino:
                if id_arista % 2 == 0:
                    self.aristas[id_arista].flujo += flujo_minimo
                    grafo_residual.aristas[id_arista].flujo -= flujo_minimo
                    grafo_residual.aristas[id_arista + 1].flujo += flujo_minimo
                else:
                    self.aristas[id_arista - 1].flujo -= flujo_minimo
                    grafo_residual.aristas[id_arista - 1].flujo -= flujo_minimo
                    grafo_residual.aristas[id_arista].flujo += flujo_minimo

            flujo += flujo_minimo

        return flujo


def ejecutar_algoritmo():
    n_vertices, n_aristas = map(int, input().split())
    grafo = GrafoDeFlujo(n_vertices)
    for _ in range(n_aristas):
        u, v, capacidad = map(int, input().split())
        grafo.agregar_arista(u - 1, v - 1, capacidad)

    print(grafo.flujo_maximo(0, n_vertices - 1))


if __name__ == "__main__":
    ejecutar_algoritmo()
