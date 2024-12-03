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
        s = "Edge(start={}, end={}, capacity={}, flow={})"\
            .format(self.inicio + 1, self.fin + 1, self.capacidad, self.flujo)
        return s

    def __repr__(self):
        s = "\nEdge(start={}, end={}, capacity={}, flow={})"\
            .format(self.inicio + 1, self.fin + 1, self.capacidad, self.flujo)
        return s


class GrafoFlujo:
    def __init__(self, n):
        self.n = n
        self.aristas = []
        self.grafo = [[] for _ in range(n)]

    def agregar_arista(self, inicio, fin, capacidad):
        arista_directa = Arista(inicio, fin, capacidad)
        arista_inversa = Arista(fin, inicio, 0)
        self.grafo[inicio].append(len(self.aristas))
        self.aristas.append(arista_directa)
        self.grafo[fin].append(len(self.aristas))
        self.aristas.append(arista_inversa)

    def encontrar_camino_corto(self, inicio, fin):
        padre = [None] * self.n
        procesado = [False] * self.n
        procesado[inicio] = True
        cola = deque([inicio])

        while cola:
            actual = cola.popleft()
            if actual == fin:
                break

            for id_arista in self.grafo[actual]:
                arista = self.aristas[id_arista]
                if not procesado[arista.fin] and arista.flujo > 0:
                    cola.append(arista.fin)
                    padre[arista.fin] = (id_arista, arista)
                    procesado[arista.fin] = True

        camino = []
        if padre[fin] is not None:
            siguiente_nodo = fin
            while siguiente_nodo != inicio:
                id_arista, arista = padre[siguiente_nodo]
                camino.append((id_arista, arista))
                siguiente_nodo = arista.inicio
            camino.reverse()
        return camino

    def maximizar_flujo(self, inicio, fin):
        grafo_residual = deepcopy(self)
        for i in range(len(grafo_residual.aristas) // 2):
            grafo_residual.aristas[i * 2].flujo = grafo_residual.aristas[i * 2].capacidad

        flujo = 0
        while True:
            camino = grafo_residual.encontrar_camino_corto(inicio, fin)
            if not camino:
                break

            flujo_minimo = camino[0][1].flujo
            for _, arista in camino[1:]:
                flujo_minimo = min(flujo_minimo, arista.flujo)

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


class EmparejamientoBipartito:
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.grafo = GrafoFlujo(n + m + 2)
        for i in range(self.n):
            self.grafo.agregar_arista(inicio=0, fin=i + 1, capacidad=1)
        for i in range(self.m):
            self.grafo.agregar_arista(inicio=self.n + 1 + i, fin=self.n + self.m + 1, capacidad=1)

    def maximizar_emparejamiento(self):
        self.grafo.maximizar_flujo(0, self.n + self.m + 1)
        emparejamientos = [-1] * self.n
        for i in range(len(self.grafo.aristas) // 2):
            arista = self.grafo.aristas[i * 2]
            if arista.inicio != 0 and arista.fin != self.n + self.m + 1 and arista.flujo == 1:
                vuelo_actual = arista.inicio - 1
                tripulacion_actual = arista.fin - self.n
                emparejamientos[vuelo_actual] = tripulacion_actual
        return emparejamientos


def algoritmo():
    num_vuelos, num_tripulaciones = map(int, input().split())
    eb = EmparejamientoBipartito(num_vuelos, num_tripulaciones)
    for i in range(num_vuelos):
        horarios = tuple(map(int, input().split()))
        for j in range(num_tripulaciones):
            if horarios[j] == 1:
                eb.grafo.agregar_arista(inicio=i + 1, fin=num_vuelos + 1 + j, capacidad=1)
    print(" ".join(map(str, eb.maximizar_emparejamiento())))


if __name__ == "__main__":
    algoritmo()
