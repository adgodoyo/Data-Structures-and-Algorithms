# Uses python3
import sys
from collections import deque, namedtuple

Nodo = namedtuple("Nodo", "v nivel")


class Grafo:
    def __init__(self, n, aristas):
        self.n = n
        self.aristas = aristas
        self.lista_adyacencia = self.obtener_lista_adyacencia(self.n, self.aristas)

    @property
    def aristas(self):
        return self._aristas

    @aristas.setter
    def aristas(self, aristas):
        nuevas_aristas = []
        for v1, v2 in aristas:
            nuevas_aristas.append((v1-1, v2-1))
        nuevas_aristas = tuple(nuevas_aristas)
        self._aristas = nuevas_aristas

    @staticmethod
    def obtener_lista_adyacencia(n, aristas):
        lista_adyacencia = {i: [] for i in range(n)}
        for v1, v2 in aristas:
            lista_adyacencia[v1].append(v2)
            lista_adyacencia[v2].append(v1)
        return lista_adyacencia

    def distancia(self, v1, v2):
        v1 -= 1
        v2 -= 1

        distancia = -1
        cola = deque([Nodo(v1, 0)])
        visitados = [False for _ in range(self.n)]
        while cola:
            actual, nivel = cola.popleft()
            if actual == v2:
                distancia = nivel
                break

            if not visitados[actual]:
                visitados[actual] = True
                for hijo in self.lista_adyacencia[actual]:
                    cola.append(Nodo(hijo, nivel+1))

        return distancia


def ejecutar_algoritmo():
    # leer datos
    datos = list(map(int, sys.stdin.read().split()))

    # procesar datos
    n, m = datos[0:2]
    datos = datos[2:]
    aristas = list(zip(datos[0:(2 * m):2], datos[1:(2 * m):2]))
    v1, v2 = datos[2 * m], datos[2 * m + 1]

    grafo = Grafo(n, aristas)
    print(grafo.distancia(v1, v2))



if __name__ == "__main__":
    ejecutar_algoritmo()
