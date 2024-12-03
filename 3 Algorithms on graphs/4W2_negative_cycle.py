# Uses python3
import sys
from collections import namedtuple
from typing import List


Test = namedtuple("Test", "n m aristas respuesta")


class Arista:
    def __init__(self, inicio, fin, peso):
        self.inicio = inicio
        self.fin = fin
        self.peso = peso


class Grafo:
    def __init__(self, num_vertices: int, num_aristas: int, aristas: List[Arista]):
        self.num_vertices = num_vertices
        self.num_aristas = num_aristas
        self.aristas = aristas
        self.lista_adyacencia = self.obtener_lista_adyacencia(self.num_vertices, self.aristas)

    @staticmethod
    def obtener_lista_adyacencia(num_vertices: int, aristas: List[Arista]) -> dict:
        lista_adyacencia = {i: [] for i in range(num_vertices)}
        for arista in aristas:
            lista_adyacencia[arista.inicio].append((arista.fin, arista.peso))
        return lista_adyacencia

    def dfs(self, vertice, visitados, orden_dfs):
        visitados[vertice] = True
        for hijo, _ in self.lista_adyacencia[vertice]:
            if not visitados[hijo]:
                self.dfs(hijo, visitados, orden_dfs)
        orden_dfs.append(vertice)

    def encontrar_componentes_fuertemente_conexas(self):
        orden_dfs = []
        visitados = [False for _ in range(self.num_vertices)]
        for vertice in range(self.num_vertices):
            if not visitados[vertice]:
                self.dfs(vertice, visitados, orden_dfs)

        aristas_invertidas = [Arista(arista.fin, arista.inicio, arista.peso) for arista in self.aristas]
        grafo_invertido = Grafo(self.num_vertices, self.num_aristas, aristas_invertidas)

        componentes = []
        visitados = [False for _ in range(self.num_vertices)]
        while orden_dfs:
            actual = orden_dfs.pop()

            if not visitados[actual]:
                componente = []
                grafo_invertido.dfs(actual, visitados, componente)
                componentes.append(componente)
        return componentes

    def tiene_ciclos_negativos(self):
        distancias = [sys.maxsize for _ in range(self.num_vertices)]
        distancias[0] = 0

        for i in range(self.num_vertices):
            for arista in self.aristas:
                nueva_distancia = distancias[arista.inicio] + arista.peso
                if nueva_distancia < distancias[arista.fin]:
                    distancias[arista.fin] = nueva_distancia
                    if i == self.num_vertices - 1:
                        return True

        return False


def ejecutar_algoritmo():
    datos = list(map(int, sys.stdin.read().split()))
    n, m = datos[0:2]
    datos = datos[2:]
    aristas = [Arista(a - 1, b - 1, w) for a, b, w in zip(datos[0::3], datos[1::3], datos[2::3])]

    grafo = Grafo(n, m, aristas)
    print(1 if grafo.tiene_ciclos_negativos() else 0)


if __name__ == "__main__":
    ejecutar_algoritmo()
