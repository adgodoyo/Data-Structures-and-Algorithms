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
        padre[inicio] = -1
        cola = deque([inicio])

        while cola:
            actual = cola.popleft()
            if actual == fin:
                break

            for id_arista in self.grafo[actual]:
                arista = self.aristas[id_arista]
                if (padre[arista.fin] is None) and (arista.flujo > 0):
                    cola.append(arista.fin)
                    padre[arista.fin] = (id_arista, arista)

        camino = []
        if padre[fin] is not None:
            siguiente_nodo = fin
            while siguiente_nodo != inicio:
                id_arista, arista = padre[siguiente_nodo]
                camino.append(id_arista)
                siguiente_nodo = arista.inicio
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

            flujo_minimo = grafo_residual.aristas[camino[0]].flujo
            for id_arista in camino[1:]:
                flujo_minimo = min(flujo_minimo, grafo_residual.aristas[id_arista].flujo)

            for id_arista in camino:
                if id_arista % 2 == 0:
                    self.aristas[id_arista].flujo += flujo_minimo
                    grafo_residual.aristas[id_arista].flujo -= flujo_minimo
                    grafo_residual.aristas[id_arista + 1].flujo += flujo_minimo
                else:
                    self.aristas[id_arista - 1].flujo -= flujo_minimo
                    grafo_residual.aristas[id_arista - 1].flujo += flujo_minimo
                    grafo_residual.aristas[id_arista].flujo -= flujo_minimo

            flujo += flujo_minimo


class EmparejamientoBipartito:
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self._id_fuente = 0
        self._id_destino = self.n + self.m + 1
        self.grafo = GrafoFlujo(self.n + self.m + 2)

        for i in range(self.n):
            self.grafo.agregar_arista(inicio=self._id_fuente, fin=i + 1, capacidad=1)

        for i in range(self.m):
            self.grafo.agregar_arista(inicio=self.n + 1 + i, fin=self._id_destino, capacidad=1)

    def maximizar_emparejamiento(self):
        self.grafo.maximizar_flujo(self._id_fuente, self._id_destino)
        emparejamientos = []
        for i in range(len(self.grafo.aristas) // 2):
            arista = self.grafo.aristas[i * 2]
            if (
                (arista.inicio != self._id_fuente)
                and (arista.fin != self._id_destino)
                and (arista.flujo == 1)
            ):
                nodo_primero = arista.inicio - 1
                nodo_segundo = arista.fin - 1
                emparejamientos.append((nodo_primero, nodo_segundo))
        return emparejamientos


class GraficasAcciones:
    def __init__(self, precios):
        self.precios = precios
        self.num_acciones = len(self.precios)
        self.num_puntos = len(self.precios[0])

    def resolver(self):
        eb = EmparejamientoBipartito(self.num_acciones, self.num_acciones)

        for i in range(self.num_acciones):
            accion_1 = self.precios[i]
            for j in range(i + 1, self.num_acciones):
                accion_2 = self.precios[j]

                arista = True
                arista_rev = True
                for k in range(self.num_puntos):
                    if arista and (accion_1[k] >= accion_2[k]):
                        arista = False
                    if arista_rev and (accion_2[k] >= accion_1[k]):
                        arista_rev = False
                    if not arista and not arista_rev:
                        break

                if arista:
                    eb.grafo.agregar_arista(i + 1, self.num_acciones + 1 + j, 1)
                if arista_rev:
                    eb.grafo.agregar_arista(j + 1, self.num_acciones + 1 + i, 1)

        emparejamientos = eb.maximizar_emparejamiento()
        num_graficas = self.num_acciones - len(emparejamientos)
        return num_graficas

def algoritmo():
    num_acciones, num_puntos = map(int, input().split())
    precios = [list(map(int, input().split())) for _ in range(num_acciones)]
    graficas = GraficasAcciones(precios)
    print(graficas.resolver())


if __name__ == "__main__":
    algoritmo()
