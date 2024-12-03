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

            actual.agregar_hijo("$", None)

    def imprimir_lista_adyacencia(self):
        cola = deque([self.arbol])

        while cola:
            actual = cola.popleft()

            if actual.valor is not None:
                print("{}->{}:{}".format(actual.padre.id_nodo, actual.id_nodo, actual.valor))

            for nodo in actual.hijos.values():
                cola.append(nodo)

    def encontrar_ocurrencias(self, texto):
        pos = 0
        posiciones_encontradas = []

        while pos < len(texto):
            nodo = self.arbol

            for c in texto[pos:]:
                if c in nodo.hijos:
                    nodo = nodo.hijos[c]

                    if "$" in nodo.hijos:
                        posiciones_encontradas.append(pos)
                        break
                else:
                    break

            pos += 1

        return posiciones_encontradas

def ejecutar_algoritmo():
    texto = sys.stdin.readline().strip()
    num_patrones = int(sys.stdin.readline())
    patrones = [sys.stdin.readline().strip() for _ in range(num_patrones)]

    arbol = Trie(patrones)
    posiciones_encontradas = arbol.encontrar_ocurrencias(texto)
    print(" ".join(map(str, posiciones_encontradas)))


if __name__ == "__main__":
    ejecutar_algoritmo()
