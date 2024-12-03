# Uses python3
import sys
from collections import namedtuple, deque
from typing import List


Test = namedtuple("Test", "n m aristas s")


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

    def distancia_mas_corta(self, s):
        distancias = [float("inf")] * self.num_vertices
        distancias[s] = 0

        for _ in range(self.num_vertices - 1):
            for arista in self.aristas:
                nueva_distancia = distancias[arista.inicio] + arista.peso
                if nueva_distancia < distancias[arista.fin]:
                    distancias[arista.fin] = nueva_distancia

        fuentes_inf_negativas = set()

        for arista in self.aristas:
            nueva_distancia = distancias[arista.inicio] + arista.peso
            if nueva_distancia < distancias[arista.fin]:
                fuentes_inf_negativas.add(arista.inicio)

        vertices_inf_negativas = set()
        cola_fuentes = deque(fuentes_inf_negativas)
        visitados = [False] * self.num_vertices
        while cola_fuentes:
            actual = cola_fuentes.popleft()
            visitados[actual] = True
            vertices_inf_negativas.add(actual)
            for hijo, _ in self.lista_adyacencia[actual]:
                if not visitados[hijo]:
                    cola_fuentes.append(hijo)

        respuesta = []
        for i in range(self.num_vertices):
            if i in vertices_inf_negativas:
                respuesta.append("-")
            elif distancias[i] == float("inf"):
                respuesta.append("*")
            else:
                respuesta.append(distancias[i])

        return respuesta


def ejecutar_algoritmo():
    datos = list(map(int, sys.stdin.read().split()))
    n, m = datos[0:2]
    datos = datos[2:]
    aristas_datos = list(zip(zip(datos[0:(3 * m):3], datos[1:(3 * m):3]), datos[2:(3 * m):3]))
    aristas = [Arista(a - 1, b - 1, w) for ((a, b), w) in aristas_datos]
    datos = datos[3 * m:]
    s = datos[0] - 1

    grafo = Grafo(n, m, aristas)
    respuesta = grafo.distancia_mas_corta(s)
    for r in respuesta:
        print(r)

if __name__ == "__main__":
    ejecutar_algoritmo()
