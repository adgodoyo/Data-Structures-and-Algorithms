# python3

import sys
import threading
sys.setrecursionlimit(10**6)  # aumentar límite de recursión
threading.stack_size(2**27)  # aumentar tamaño del stack para un nuevo hilo

class TreeOrders:
    def read(self):
        self.n = int(sys.stdin.readline())
        self.key = [0] * self.n
        self.left = [0] * self.n
        self.right = [0] * self.n
        for i in range(self.n):
            [a, b, c] = map(int, sys.stdin.readline().split())
            self.key[i] = a
            self.left[i] = b
            self.right[i] = c

    def inOrder(self):
        self.result = []
        self._in_order_traversal(0)  # comenzar desde el nodo raíz (índice 0)
        return self.result

    def _in_order_traversal(self, node):
        if node == -1:  # si es un hijo nulo, regresar
            return
        self._in_order_traversal(self.left[node])  # recorrer el subárbol izquierdo
        self.result.append(self.key[node])  # procesar el nodo actual
        self._in_order_traversal(self.right[node])  # recorrer el subárbol derecho

    def preOrder(self):
        self.result = []
        self._pre_order_traversal(0)  # comenzar desde el nodo raíz (índice 0)
        return self.result

    def _pre_order_traversal(self, node):
        if node == -1:  # si es un hijo nulo, regresar
            return
        self.result.append(self.key[node])  # procesar el nodo actual
        self._pre_order_traversal(self.left[node])  # recorrer el subárbol izquierdo
        self._pre_order_traversal(self.right[node])  # recorrer el subárbol derecho

    def postOrder(self):
        self.result = []
        self._post_order_traversal(0)  # comenzar desde el nodo raíz (índice 0)
        return self.result

    def _post_order_traversal(self, node):
        if node == -1:  # si es un hijo nulo, regresar
            return
        self._post_order_traversal(self.left[node])  # recorrer el subárbol izquierdo
        self._post_order_traversal(self.right[node])  # recorrer el subárbol derecho
        self.result.append(self.key[node])  # procesar el nodo actual

def main():
    tree = TreeOrders()
    tree.read()
    print(" ".join(str(x) for x in tree.inOrder()))
    print(" ".join(str(x) for x in tree.preOrder()))
    print(" ".join(str(x) for x in tree.postOrder()))

# Ejecutar en un hilo separado para manejar el límite del stack
threading.Thread(target=main).start()
