# Uses python3
import sys
from collections import deque


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

    def es_bipartito(self):
        es_bipartito = True

        visitados = [False for _ in range(self.n)]
        color = [False for _ in range(self.n)]

        for v in range(self.n):
            cola = deque([v])
            while cola:
                actual = cola.popleft()
                if not visitados[actual]:
                    visitados[actual] = True

                    for hijo in self.lista_adyacencia[actual]:
                        if visitados[hijo]:
                            if color[hijo] == color[actual]:
                                es_bipartito = False
                                break
                        else:
                            cola.append(hijo)
                            color[hijo] = not color[actual]

                if not es_bipartito:
                    break

            if not es_bipartito:
                break

        return es_bipartito


def ejecutar_algoritmo():
    # leer datos
    datos = list(map(int, sys.stdin.read().split()))

    # procesar datos
    n, m = datos[0:2]
    datos = datos[2:]
    aristas = list(zip(datos[0:(2 * m):2], datos[1:(2 * m):2]))

    grafo = Grafo(n, aristas)
    print(1 if grafo.es_bipartito() else 0)


def ejecutar_prueba():
    # Pruebas de ejemplo
    n, m = 4, 4
    aristas = (
        (1, 2),
        (4, 1),
        (2, 3),
        (3, 1),
    )

    grafo = Grafo(n, aristas)
    print(1 if grafo.es_bipartito() else 0)


if __name__ == "__main__":
    ejecutar_algoritmo()
