# Uses python3

import sys

sys.setrecursionlimit(200000)


class Grafo:
    def __init__(self, n, m, aristas):
        self.n = n  # número de vértices
        self.m = m  # número de aristas
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
        for v_inicio, v_fin in aristas:
            lista_adyacencia[v_inicio].append(v_fin)
        return lista_adyacencia

    def dfs(self, v, visitados, orden_dfs):
        visitados[v] = True
        for hijo in self.lista_adyacencia[v]:
            if not visitados[hijo]:
                self.dfs(hijo, visitados, orden_dfs)
        orden_dfs.append(v)

    def encontrar_componentes_fuertemente_conexas(self):
        orden_dfs = []
        visitados = [False for _ in range(self.n)]
        for v in range(self.n):
            if not visitados[v]:
                self.dfs(v, visitados, orden_dfs)

        aristas_invertidas = tuple((b+1, a+1) for (a, b) in self.aristas)
        grafo_invertido = Grafo(self.n, self.m, aristas_invertidas)

        componentes_conexas = []
        visitados = [False for _ in range(self.n)]
        while orden_dfs:
            actual = orden_dfs.pop()
            componente = []

            if not visitados[actual]:
                grafo_invertido.dfs(actual, visitados, componente)

            if componente:
                componentes_conexas.append(componente)
        return componentes_conexas


def ejecutar_algoritmo():
    # leer datos
    datos = list(map(int, sys.stdin.read().split()))

    # procesar datos
    n, m = datos[0:2]
    datos = datos[2:]
    aristas = list(zip(datos[0:(2 * m):2], datos[1:(2 * m):2]))

    grafo = Grafo(n, m, aristas)
    print(len(grafo.encontrar_componentes_fuertemente_conexas()))

if __name__ == "__main__":
    ejecutar_algoritmo()
