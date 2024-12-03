# Uses python3
import sys
from collections import namedtuple, deque

Prueba = namedtuple("Prueba", "n m u v aristas salida")


class Grafo:
    def __init__(self, n, m, aristas):
        self.n = n  # número de vértices
        self.m = m  # número de aristas
        self.aristas = aristas

        self._aristas = []
        for v1, v2 in self.aristas:
            self._aristas.append((v1 - 1, v2 - 1))

        self.lista_adyacencia = self.crear_lista_adyacencia(self.n, self._aristas)

        self.numero_componentes = 0
        self.componentes_conexas = self.crear_componentes_conexas()

    @staticmethod
    def crear_lista_adyacencia(n, aristas):
        lista_adyacencia = {i: set() for i in range(n)}
        for v1, v2 in aristas:
            lista_adyacencia[v1].add(v2)
            lista_adyacencia[v2].add(v1)
        return lista_adyacencia

    def crear_componentes_conexas(self):
        componentes = [-1 for _ in range(self.n)]
        visitados = [False for _ in range(self.n)]

        indice_cc = 0

        for vertice, vecinos in self.lista_adyacencia.items():
            if not visitados[vertice]:
                visitados[vertice] = True
                componentes[vertice] = indice_cc

                cola = deque(vecinos)
                while cola:
                    actual = cola.popleft()
                    visitados[actual] = True
                    componentes[actual] = indice_cc
                    for vecino in self.lista_adyacencia[actual]:
                        if not visitados[vecino]:
                            cola.append(vecino)

                indice_cc += 1

        self.numero_componentes = indice_cc
        return componentes

    def existe_camino(self, v1, v2):
        v1 -= 1
        v2 -= 1

        return 1 if self.componentes_conexas[v1] == self.componentes_conexas[v2] else 0


def ejecutar_algoritmo():
    # leer datos
    datos = list(map(int, sys.stdin.read().split()))

    # procesar datos
    n, m = datos[0:2]
    datos = datos[2:]
    aristas = list(zip(datos[0:(2 * m):2], datos[1:(2 * m):2]))

    grafo = Grafo(n, m, aristas)
    print(grafo.numero_componentes)


if __name__ == "__main__":
    ejecutar_algoritmo()
