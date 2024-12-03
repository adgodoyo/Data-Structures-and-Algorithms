# python 3
from collections import deque
from random import randint, choice


class AristaFG:
    def __init__(self, inicio, fin, capacidad):
        self.inicio = inicio
        self.fin = fin
        self.capacidad = capacidad
        self.flujo = 0

    def __str__(self):
        s = "Arista(inicio={}, fin={}, capacidad={}, flujo={})"\
            .format(self.inicio + 1, self.fin + 1, self.capacidad, self.flujo)
        return s

    def __repr__(self):
        s = "\nArista(inicio={}, fin={}, capacidad={}, flujo={})"\
            .format(self.inicio + 1, self.fin + 1, self.capacidad, self.flujo)
        return s


class GrafoFlujo:
    INF = 10 ** 6

    def __init__(self, n):
        self.n = n
        self.aristas = []
        self.grafo = [[] for _ in range(n)]

    def agregar_arista(self, inicio, fin, capacidad):
        arista_directa = AristaFG(inicio, fin, capacidad)
        arista_inversa = AristaFG(fin, inicio, 0)
        self.grafo[inicio].append(len(self.aristas))
        self.aristas.append(arista_directa)
        self.grafo[fin].append(len(self.aristas))
        self.aristas.append(arista_inversa)

    def encontrar_camino_mas_corto(self, inicio, fin):
        arista_previa = [None] * self.n
        procesado = [False] * self.n
        procesado[inicio] = True

        cola = deque([inicio])
        while cola:
            actual = cola.popleft()
            if actual == fin:
                break

            for id_arista in self.grafo[actual]:
                arista = self.aristas[id_arista]
                if (not procesado[arista.fin]) and (arista.flujo < arista.capacidad):
                    cola.append(arista.fin)
                    arista_previa[arista.fin] = id_arista
                    procesado[arista.fin] = True

        camino = None
        if arista_previa[fin] is not None:
            camino = []
            nodo = fin
            while nodo != inicio:
                id_arista = arista_previa[nodo]
                camino.append(id_arista)
                nodo = self.aristas[id_arista].inicio
            camino.reverse()
        return camino

    def maximizar_flujo(self, inicio, fin):
        while True:
            camino = self.encontrar_camino_mas_corto(inicio, fin)
            if camino is None:
                break

            flujo_minimo = GrafoFlujo.INF
            for id_arista in camino:
                arista = self.aristas[id_arista]
                flujo_minimo = min(flujo_minimo, arista.capacidad - arista.flujo)

            for id_arista in camino:
                if id_arista % 2 == 0:
                    self.aristas[id_arista].capacidad -= flujo_minimo
                    self.aristas[id_arista + 1].capacidad += flujo_minimo
                else:
                    self.aristas[id_arista - 1].capacidad += flujo_minimo
                    self.aristas[id_arista].capacidad -= flujo_minimo

        for i in range(len(self.aristas) // 2):
            self.aristas[i * 2].flujo = self.aristas[i * 2 + 1].capacidad
            self.aristas[i * 2].capacidad += self.aristas[i * 2 + 1].capacidad


class AristaNC:
    def __init__(self, inicio, fin, limite_inferior, capacidad):
        self.inicio = inicio
        self.fin = fin
        self.limite_inferior = limite_inferior
        self.capacidad = capacidad
        self.flujo = 0

    def __str__(self):
        s = "Arista(inicio={}, fin={}, limite_inferior={}, capacidad={})"\
            .format(self.inicio, self.fin, self.limite_inferior, self.capacidad)
        return s

    def __repr__(self):
        s = "Arista(inicio={}, fin={}, limite_inferior={}, capacidad={})" \
            .format(self.inicio, self.fin, self.limite_inferior, self.capacidad)
        return s


class CirculacionRed:
    def __init__(self, n_vertices, aristas):
        self.n = n_vertices
        self.aristas = aristas
        self.m = len(self.aristas)

    def resolver(self):
        if self.verificar_solucion_naive():
            circulacion = []
            for arista in self.aristas:
                arista.flujo = arista.limite_inferior
                circulacion.append(arista.flujo)
            return circulacion

        lista_prev = [[] for _ in range(self.n)]
        lista_sig = [[] for _ in range(self.n)]
        for i, arista in enumerate(self.aristas):
            lista_prev[arista.fin].append(i)
            lista_sig[arista.inicio].append(i)

        gf = GrafoFlujo(self.n + 2)
        for arista in self.aristas:
            gf.agregar_arista(arista.inicio, arista.fin, arista.capacidad - arista.limite_inferior)

        demandas = [0] * self.n
        for v in range(self.n):
            demandas[v] -= sum([self.aristas[i].limite_inferior for i in lista_prev[v]])
            demandas[v] += sum([self.aristas[i].limite_inferior for i in lista_sig[v]])

        for v in range(self.n):
            demanda = demandas[v]
            if demanda < 0:
                gf.agregar_arista(self.n, v, abs(demanda))
            elif demanda > 0:
                gf.agregar_arista(v, self.n + 1, demanda)

        gf.maximizar_flujo(inicio=self.n, fin=self.n + 1)

        for arista in gf.aristas:
            if (arista.inicio == self.n) and (arista.flujo != arista.capacidad):
                return None
            elif (arista.fin == self.n + 1) and (arista.flujo != arista.capacidad):
                return None

        circulacion = []
        for i, arista in enumerate(self.aristas):
            arista.flujo = arista.limite_inferior + gf.aristas[i * 2].flujo
            circulacion.append(arista.flujo)
        return circulacion

    def verificar_solucion_naive(self):
        flujo_original = []
        for arista in self.aristas:
            flujo_original.append(arista.flujo)
            arista.flujo = arista.limite_inferior

        resultado = self.verificar_solucion(self.n, self.aristas)

        for i, arista in enumerate(self.aristas):
            arista.flujo = flujo_original[i]
        return resultado

    @staticmethod
    def verificar_solucion(n, aristas):
        for arista in aristas:
            if arista.limite_inferior <= arista.flujo <= arista.capacidad:
                continue
            else:
                return False

        lista_prev = [[] for _ in range(n)]
        lista_sig = [[] for _ in range(n)]
        for i, arista in enumerate(aristas):
            lista_prev[arista.fin].append(i)
            lista_sig[arista.inicio].append(i)

        for v in range(n):
            entrada = sum([aristas[i].flujo for i in lista_prev[v]])
            salida = sum([aristas[i].flujo for i in lista_sig[v]])
            if entrada != salida:
                return False
        return True


def ejecutar_algoritmo():
    n_vertices, n_aristas = map(int, input().split())
    aristas = []
    for _ in range(n_aristas):
        v1, v2, limite_inf, capacidad = map(int, input().split())
        aristas.append(AristaNC(v1 - 1, v2 - 1, limite_inf, capacidad))
    aristas = tuple(aristas)

    circulacion = CirculacionRed(n_vertices, aristas).resolver()

    if circulacion is not None:
        print("YES")
        for flujo in circulacion:
            print(flujo)
    else:
        print("NO")


if __name__ == "__main__":
    ejecutar_algoritmo()
