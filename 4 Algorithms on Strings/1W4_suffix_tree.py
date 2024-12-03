# Uses python3
import sys
from collections import deque


class NodoArbol:
    def __init__(self, padre, inicio, longitud):
        self.padre = padre
        self.inicio = inicio
        self.longitud = longitud
        self.hijos = []

    def agregar_hijo(self, inicio, longitud):
        self.hijos.append(NodoArbol(self, inicio, longitud))


class ArbolDeSufijos:
    def __init__(self, texto):
        self.texto = texto
        self.arbol = self._construir_arbol(self.texto)

    @staticmethod
    def _construir_arbol(texto):
        ultima_posicion = len(texto) - 1

        raiz = NodoArbol(
            padre=None,
            inicio=None,
            longitud=None,
        )

        posicion = 0
        while posicion <= ultima_posicion:
            nodo_actual = raiz

            posicion_interna = posicion
            while posicion_interna <= ultima_posicion:
                hijo_compatible = None
                for i, hijo in enumerate(nodo_actual.hijos):
                    if texto[posicion_interna] == texto[hijo.inicio]:
                        hijo_compatible = i

                if hijo_compatible is not None:
                    hijo = nodo_actual.hijos[hijo_compatible]
                    siguiente_nodo = hijo
                    for j in range(hijo.longitud):
                        pos_hijo = hijo.inicio + j
                        if texto[posicion_interna] != texto[pos_hijo]:
                            nodo_dividido = NodoArbol(nodo_actual, hijo.inicio, j)
                            nodo_dividido.hijos = [hijo]

                            nodo_actual.hijos.pop(hijo_compatible)
                            nodo_actual.hijos.append(nodo_dividido)

                            hijo.padre = nodo_dividido
                            hijo.inicio = pos_hijo
                            hijo.longitud -= j

                            siguiente_nodo = nodo_dividido
                            break

                        posicion_interna += 1

                    nodo_actual = siguiente_nodo
                else:
                    nodo_actual.agregar_hijo(posicion_interna, ultima_posicion - posicion_interna + 1)
                    posicion_interna = ultima_posicion + 1

            posicion += 1

        return raiz

    def imprimir(self):
        cola = deque(self.arbol.hijos)

        while cola:
            actual = cola.popleft()
            print(self.texto[actual.inicio:(actual.inicio + actual.longitud)])
            for hijo in actual.hijos:
                cola.append(hijo)

def ejecutar_algoritmo():
    texto = sys.stdin.readline().strip()
    arbol = ArbolDeSufijos(texto)
    arbol.imprimir()


if __name__ == "__main__":
    ejecutar_algoritmo()
