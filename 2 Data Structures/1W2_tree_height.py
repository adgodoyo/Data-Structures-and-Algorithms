import sys
import threading

def compute_height(n, parents):
    # Crear una lista para almacenar la altura calculada de cada nodo
    heights = [0] * n

    def get_height(node):
        # Si ya hemos calculado la altura para este nodo, la devolvemos
        if heights[node] != 0:
            return heights[node]

        # Si el nodo es la raíz
        if parents[node] == -1:
            heights[node] = 1
        else:
            # Altura es 1 + altura del padre
            heights[node] = 1 + get_height(parents[node])
        
        return heights[node]

    # Calcular la altura para todos los nodos
    max_height = 0
    for node in range(n):
        max_height = max(max_height, get_height(node))

    return max_height


def main():
    n = int(input())
    parents = list(map(int, input().split()))
    print(compute_height(n, parents))


# Ajustar los límites de recursión y tamaño de pila
sys.setrecursionlimit(10**7)
threading.stack_size(2**27)
threading.Thread(target=main).start()
