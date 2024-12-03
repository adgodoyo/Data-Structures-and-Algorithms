# Uses python3
import sys
from collections import namedtuple
from typing import List


Test = namedtuple("Test", "n m aristas inicio fin respuesta")


class ElementoColaDijkstra:
    def __init__(self, vertice, distancia):
        self.vertice = vertice
        self.distancia = distancia


class ColaPrioridadDijkstra:
    def __init__(self):
        self.q = []
        self.vacia = True
        self.num_elementos = 0
        self.indices_vertices = dict()

    def insertar(self, elem):
        self.q.append(elem)
        self.num_elementos += 1
        self.vacia = False
        self.indices_vertices[elem.vertice] = self.num_elementos - 1
        self.subir(self.num_elementos - 1)

    def extraer_minimo(self):
        elemento_min = None

        if self.num_elementos > 0:
            if self.num_elementos == 1:
                elemento_min = self.q.pop()
            else:
                elemento_min = self.q[0]
                ultimo_elem = self.q.pop()
                self.q[0] = ultimo_elem
                self.indices_vertices[ultimo_elem.vertice] = 0

            self.num_elementos -= 1
            if self.num_elementos == 0:
                self.vacia = True
            del self.indices_vertices[elemento_min.vertice]

            self.bajar(0)

        return elemento_min

    def cambiar_distancia(self, vertice, nueva_distancia):
        i = self.indices_vertices[vertice]

        distancia_actual = self.q[i].distancia
        self.q[i].distancia = nueva_distancia
        if nueva_distancia >= distancia_actual:
            self.bajar(i)
        else:
            self.subir(i)

    def hijo_izquierdo_i(self, i):
        j = 2 * i + 1
        if j >= self.num_elementos:
            j = None
        return j

    def hijo_derecho_i(self, i):
        j = 2 * i + 2
        if j >= self.num_elementos:
            j = None
        return j

    @staticmethod
    def padre_i(i):
        j = (i - 1) // 2
        if i == 0:
            j = None
        return j

    def bajar(self, i):
        while True:
            lci = self.hijo_izquierdo_i(i)
            rci = self.hijo_derecho_i(i)

            if (lci is not None) and (rci is not None):
                if self.q[lci].distancia == self.q[i].distancia == self.q[rci].distancia:
                    break
                elif (self.q[lci].distancia <= self.q[i].distancia) and (self.q[lci].distancia <= self.q[rci].distancia):
                    self.q[i], self.q[lci] = self.q[lci], self.q[i]
                    self.indices_vertices[self.q[i].vertice] = i
                    self.indices_vertices[self.q[lci].vertice] = lci
                    i = lci
                elif (self.q[rci].distancia <= self.q[i].distancia) and (self.q[rci].distancia <= self.q[lci].distancia):
                    self.q[i], self.q[rci] = self.q[rci], self.q[i]
                    self.indices_vertices[self.q[i].vertice] = i
                    self.indices_vertices[self.q[rci].vertice] = rci
                    i = rci
                else:
                    break
            elif lci is not None:
                if self.q[lci].distancia < self.q[i].distancia:
                    self.q[i], self.q[lci] = self.q[lci], self.q[i]
                    self.indices_vertices[self.q[i].vertice] = i
                    self.indices_vertices[self.q[lci].vertice] = lci
                    i = lci
                else:
                    break
            else:
                break

    def subir(self, i):
        while True:
            if i == 0:
                break

            pi = self.padre_i(i)
            if self.q[i].distancia < self.q[pi].distancia:
                self.q[i], self.q[pi] = self.q[pi], self.q[i]
                self.indices_vertices[self.q[i].vertice] = i
                self.indices_vertices[self.q[pi].vertice] = pi
                i = pi
            else:
                break


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

    def dijkstra(self, inicio, fin):
        dist = [float("inf")] * self.num_vertices
        procesado = [False] * self.num_vertices
        finalizado = [False] * self.num_vertices

        cola = ColaPrioridadDijkstra()
        cola.insertar(ElementoColaDijkstra(inicio, 0))
        dist[inicio] = 0
        procesado[inicio] = True

        while not cola.vacia:
            actual = cola.extraer_minimo()
            finalizado[actual.vertice] = True

            if actual.vertice == fin:
                break

            hijos = self.lista_adyacencia[actual.vertice]
            for hijo, peso in hijos:
                if not finalizado[hijo]:
                    nueva_distancia = dist[actual.vertice] + peso

                    if not procesado[hijo]:
                        dist[hijo] = nueva_distancia
                        cola.insertar(ElementoColaDijkstra(hijo, nueva_distancia))
                        procesado[hijo] = True
                    else:
                        if nueva_distancia < dist[hijo]:
                            dist[hijo] = nueva_distancia
                            cola.cambiar_distancia(hijo, nueva_distancia)

        return dist[fin] if finalizado[fin] else -1


def ejecutar_algoritmo():
    datos = list(map(int, sys.stdin.read().split()))
    n, m = datos[0:2]
    datos = datos[2:]
    aristas_datos = list(zip(zip(datos[0:(3 * m):3], datos[1:(3 * m):3]), datos[2:(3 * m):3]))
    datos = datos[3 * m:]
    aristas = []
    for ((a, b), w) in aristas_datos:
        aristas.append(Arista(a - 1, b - 1, w))
    inicio, fin = datos[0] - 1, datos[1] - 1

    grafo = Grafo(n, m, aristas)
    print(grafo.dijkstra(inicio, fin))


if __name__ == "__main__":
    ejecutar_algoritmo()
