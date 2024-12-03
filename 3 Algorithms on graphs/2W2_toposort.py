# Uses python3

import sys


class Grafo:
    def __init__(self, n, m, aristas):
        self.n = n  # número de vértices
        self.m = m  # número de aristas
        self.aristas = aristas
        self.lista_adyacencia, self.fuentes = self.obtener_lista_adyacencia_y_fuentes(self.n, self.aristas)

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
    def obtener_lista_adyacencia_y_fuentes(n, aristas):
        lista_adyacencia = {i: [] for i in range(n)}
        fuentes = [True for _ in range(n)]
        for v_inicio, v_fin in aristas:
            lista_adyacencia[v_inicio].append(v_fin)
            fuentes[v_fin] = False

        fuentes = tuple([i for i in range(n) if fuentes[i]])
        return lista_adyacencia, fuentes

    def orden_topologico(self):
        visitados = [False for _ in range(self.n)]
        resultado = []
        for fuente in self.fuentes:
            self.dfs(fuente, visitados, resultado)

        resultado = list(reversed(resultado))
        resultado = [a+1 for a in resultado]
        return resultado

    def dfs(self, fuente, visitados, resultado):
        for hijo in self.lista_adyacencia[fuente]:
            if not visitados[hijo]:
                self.dfs(hijo, visitados, resultado)
        visitados[fuente] = True
        resultado.append(fuente)


def ejecutar_algoritmo():
    # leer datos
    datos = list(map(int, sys.stdin.read().split()))

    # procesar datos
    n, m = datos[0:2]
    datos = datos[2:]
    aristas = list(zip(datos[0:(2 * m):2], datos[1:(2 * m):2]))

    grafo = Grafo(n, m, aristas)
    print(" ".join(map(str, grafo.orden_topologico())))


if __name__ == "__main__":
    ejecutar_algoritmo()
