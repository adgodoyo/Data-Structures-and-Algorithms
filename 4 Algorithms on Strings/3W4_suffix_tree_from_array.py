# python3
import sys
from collections import deque


class NodoArbolDeSufijos:
    def __init__(self, padre, profundidad_cadena, inicio_arista, fin_arista):
        self.padre = padre
        self.profundidad_cadena = profundidad_cadena
        self.inicio_arista = inicio_arista
        self.fin_arista = fin_arista
        self.hijos = dict()
        self.id_nodo = None


class ArbolDeSufijos:
    def __init__(self, texto, arreglo_sufijos, lcp, alfabeto):
        self.texto = texto
        self.arreglo_sufijos = arreglo_sufijos
        self.lcp = lcp
        self.alfabeto = sorted(alfabeto)
        self.raiz = self._construir_arbol(self.texto, self.arreglo_sufijos, self.lcp)
        self.aristas = self._construir_aristas(self.raiz)

    def _construir_aristas(self, raiz):
        aristas = dict()
        raiz.id_nodo = 0
        id_actual = 1
        cola = deque([raiz])
        while cola:
            actual = cola.popleft()
            if actual.hijos:
                aristas[actual.id_nodo] = []
                for char in self.alfabeto:
                    if char in actual.hijos:
                        hijo = actual.hijos[char]
                        hijo.id_nodo = id_actual
                        id_actual += 1
                        aristas[actual.id_nodo].append((hijo.id_nodo, hijo.inicio_arista, hijo.fin_arista))
                        cola.append(hijo)
        return aristas

    def _construir_arbol(self, texto, arreglo_sufijos, lcp):
        raiz = NodoArbolDeSufijos(None, 0, -1, -1)
        lcp_anterior = 0
        nodo_actual = raiz

        for i in range(len(texto)):
            sufijo = arreglo_sufijos[i]

            while nodo_actual.profundidad_cadena > lcp_anterior:
                nodo_actual = nodo_actual.padre

            if nodo_actual.profundidad_cadena == lcp_anterior:
                nodo_actual = self._crear_nueva_hoja(nodo_actual, texto, sufijo)
            else:
                inicio_arista = arreglo_sufijos[i - 1] + nodo_actual.profundidad_cadena
                desplazamiento = lcp_anterior - nodo_actual.profundidad_cadena
                nodo_intermedio = self._dividir_arista(nodo_actual, texto, inicio_arista, desplazamiento)
                nodo_actual = self._crear_nueva_hoja(nodo_intermedio, texto, sufijo)

            if i < len(texto) - 1:
                lcp_anterior = lcp[i]

        return raiz

    @staticmethod
    def _crear_nueva_hoja(nodo, texto, sufijo):
        hoja = NodoArbolDeSufijos(
            padre=nodo,
            profundidad_cadena=len(texto) - sufijo,
            inicio_arista=nodo.profundidad_cadena + sufijo,
            fin_arista=len(texto) - 1,
        )
        nodo.hijos[texto[hoja.inicio_arista]] = hoja
        return hoja

    @staticmethod
    def _dividir_arista(nodo, texto, inicio, desplazamiento):
        char_inicio = texto[inicio]
        char_medio = texto[inicio + desplazamiento]
        nodo_intermedio = NodoArbolDeSufijos(
            padre=nodo,
            profundidad_cadena=nodo.profundidad_cadena + desplazamiento,
            inicio_arista=inicio,
            fin_arista=inicio + desplazamiento - 1,
        )
        nodo_intermedio.hijos[char_medio] = nodo.hijos[char_inicio]
        nodo.hijos[char_inicio].padre = nodo_intermedio
        nodo.hijos[char_inicio].inicio_arista += desplazamiento
        nodo.hijos[char_inicio] = nodo_intermedio
        return nodo_intermedio

    def salida_arbol(self):
        pila = [(0, 0)]
        while pila:
            nodo, indice_arista = pila.pop()
            if nodo not in self.aristas:
                continue
            aristas = self.aristas[nodo]
            if indice_arista + 1 < len(aristas):
                pila.append((nodo, indice_arista + 1))
            print("%d %d" % (aristas[indice_arista][1], aristas[indice_arista][2] + 1))
            pila.append((aristas[indice_arista][0], 0))

def ejecutar_algoritmo():
    alfabeto = "ACGT$"
    texto = sys.stdin.readline().strip()
    arreglo_sufijos = list(map(int, sys.stdin.readline().strip().split()))
    lcp = list(map(int, sys.stdin.readline().strip().split()))
    print(texto)
    arbol = ArbolDeSufijos(texto, arreglo_sufijos, lcp, alfabeto)
    arbol.salida_arbol()


if __name__ == "__main__":
    ejecutar_algoritmo()
