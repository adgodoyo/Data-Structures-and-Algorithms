import sys
import threading

sys.setrecursionlimit(10 ** 8)  # Profundidad máxima de recursión
threading.stack_size(2 ** 27)  # Nuevo hilo con un tamaño de pila específico


class Nodo:
    def __init__(self, clave, izquierda=None, derecha=None):
        self.clave = clave
        self.izquierda = izquierda if izquierda != -1 else None
        self.derecha = derecha if derecha != -1 else None


class ArbolEsBST:
    def __init__(self):
        self.nodos = []
        self.raiz = None
        self.resultado_inorden = []

    def leer(self):
        cantidad_nodos = int(sys.stdin.readline().strip())

        for _ in range(cantidad_nodos):
            clave, izquierda, derecha = map(int, sys.stdin.readline().split())
            nodo = Nodo(clave, izquierda, derecha)
            self.nodos.append(nodo)

        if cantidad_nodos > 0:
            self.raiz = self.nodos[0]

    def recorrido_inorden(self, nodo):
        if not nodo:
            return

        if nodo.izquierda:
            self.recorrido_inorden(self.nodos[nodo.izquierda])

        self.resultado_inorden.append(nodo.clave)

        if nodo.derecha:
            self.recorrido_inorden(self.nodos[nodo.derecha])

    def es_bst(self):
        if len(self.nodos) <= 1:  # Un árbol vacío o con un solo nodo es BST
            return True

        self.recorrido_inorden(self.raiz)

        # Verificar que la lista resultante esté en orden ascendente estricto
        return all(self.resultado_inorden[i] < self.resultado_inorden[i+1]
                   for i in range(len(self.resultado_inorden) - 1))


def main():
    arbol = ArbolEsBST()
    arbol.leer()
    if arbol.es_bst():
        print("CORRECT")
    else:
        print("INCORRECT")


if __name__ == "__main__":
    threading.Thread(target=main).start()

