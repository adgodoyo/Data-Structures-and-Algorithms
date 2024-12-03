# Uses python3
import sys
from collections import deque


class NodoTrie:
    def __init__(self, padre, valor, id_nodo):
        self.padre = padre
        self.valor = valor
        self.id_nodo = id_nodo
        self.hijos = dict()

    def agregar_hijo(self, valor, id_nodo):
        self.hijos[valor] = NodoTrie(self, valor, id_nodo)


class Trie:
    def __init__(self, patrones):
        self.patrones = patrones
        self.arbol = NodoTrie(None, None, 0)
        self._construir_trie(self.patrones)

    def _construir_trie(self, patrones):
        id_nodo = 1

        for patron in patrones:
            actual = self.arbol
            for c in patron:
                if c not in actual.hijos:
                    actual.agregar_hijo(c, id_nodo)
                    id_nodo += 1

                actual = actual.hijos[c]

    def imprimir_lista_adyacencia(self):
        cola = deque([self.arbol])

        while cola:
            actual = cola.popleft()

            if actual.valor is not None:
                print("{}->{}:{}".format(actual.padre.id_nodo, actual.id_nodo, actual.valor))

            for nodo in actual.hijos.values():
                cola.append(nodo)

def ejecutar_algoritmo():
    patrones = sys.stdin.read().split()[1:]
    arbol = Trie(patrones)
    arbol.imprimir_lista_adyacencia()


if __name__ == "__main__":
    ejecutar_algoritmo()
