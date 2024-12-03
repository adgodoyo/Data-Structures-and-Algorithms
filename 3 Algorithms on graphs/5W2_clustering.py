# Uses python3
import sys
from math import sqrt


class Punto:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"


class Arista:
    def __init__(self, inicio, fin, p_inicio, p_fin):
        self.inicio = inicio
        self.fin = fin
        self.p_inicio = p_inicio
        self.p_fin = p_fin
        self.peso = sqrt((p_fin.x - p_inicio.x)**2 + (p_fin.y - p_inicio.y)**2)

    def __str__(self):
        return f"Arista {self.inicio}-{self.fin} peso={self.peso:.2f}"


class ConjuntoDisjunto:
    def __init__(self, n):
        self.n = n
        self.conjuntos = [i for i in range(n)]
        self.num_conjuntos = self.n

    def encontrar(self, i):
        while self.conjuntos[i] != i:
            anterior = i
            i = self.conjuntos[i]
            self.conjuntos[anterior] = i  # compresión de caminos
        return i

    def unir(self, i, j):
        padre_i = self.encontrar(i)
        padre_j = self.encontrar(j)

        if padre_i != padre_j:
            self.conjuntos[padre_j] = padre_i
            self.num_conjuntos -= 1


def agrupar(x, y, k):
    respuesta = float("inf")
    n = len(x)

    # crear todas las aristas con sus pesos
    aristas = []
    for i in range(n):
        for j in range(i + 1, n):
            aristas.append(Arista(i, j, Punto(x[i], y[i]), Punto(x[j], y[j])))

    # ordenar aristas por peso
    aristas = sorted(aristas, key=lambda arista: arista.peso)

    cd = ConjuntoDisjunto(n)

    for arista in aristas:
        if cd.encontrar(arista.inicio) != cd.encontrar(arista.fin):
            if cd.num_conjuntos > k:
                cd.unir(arista.inicio, arista.fin)
            else:
                respuesta = min(respuesta, arista.peso)

    return respuesta


def ejecutar_algoritmo():
    datos = list(map(int, sys.stdin.read().split()))
    n = datos[0]
    datos = datos[1:]
    x = datos[0:2 * n:2]
    y = datos[1:2 * n:2]
    datos = datos[2 * n:]
    k = datos[0]
    print("{0:.9f}".format(agrupar(x, y, k)))

if __name__ == "__main__":
    ejecutar_algoritmo()
