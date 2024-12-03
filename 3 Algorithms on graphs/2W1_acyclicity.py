# Uses python3

import sys
from collections import deque


class Grafo:
    def __init__(self, n, m, aristas):
        self.n = n  # número de vértices
        self.m = m  # número de aristas
        self.aristas = aristas
        self.lista_adyacencia = self.obtener_lista_adyacencia(self.n, self.aristas)
        self.ciclico = 1 if self.es_ciclico() else 0

    @property
    def aristas(self):
        return self._aristas

    @aristas.setter
    def aristas(self, aristas):
        aristas_nuevas = []
        for v1, v2 in aristas:
            aristas_nuevas.append((v1-1, v2-1))
        aristas_nuevas = tuple(aristas_nuevas)
        self._aristas = aristas_nuevas

    @staticmethod
    def obtener_lista_adyacencia(n, aristas):
        lista_adyacencia = {i: [] for i in range(n)}
        for v_inicio, v_fin in aristas:
            lista_adyacencia[v_inicio].append(v_fin)
        return lista_adyacencia

    def es_ciclico(self):
        ciclico = False
        for vertice, hijos in self.lista_adyacencia.items():
            visitados = [False for _ in range(self.n)]
            visitados[vertice] = True
            cola = deque(hijos)
            while cola:
                actual = cola.popleft()

                if actual == vertice:
                    ciclico = True
                    break

                if not visitados[actual]:
                    visitados[actual] = True
                    for hijo in self.lista_adyacencia[actual]:
                        cola.append(hijo)

            if ciclico:
                break
        return ciclico


def ejecutar_algoritmo():
    # leer datos
    datos = list(map(int, sys.stdin.read().split()))

    # procesar datos
    n, m = datos[0:2]
    datos = datos[2:]
    aristas = list(zip(datos[0:(2 * m):2], datos[1:(2 * m):2]))

    grafo = Grafo(n, m, aristas)
    print(grafo.ciclico)


if __name__ == "__main__":
    ejecutar_algoritmo()
