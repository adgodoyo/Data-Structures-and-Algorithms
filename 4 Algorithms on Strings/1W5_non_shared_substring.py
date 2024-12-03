# Uses python3
import sys
from collections import deque


class NodoArbol:
    def __init__(self, padre, inicio, longitud, inicio_inicial):
        self.padre = padre
        self.inicio = inicio
        self.longitud = longitud
        self.inicio_inicial = inicio_inicial
        self.hijos = []
        self.tipo_texto = None

    def agregar_hijo(self, inicio, longitud, inicio_inicial):
        self.hijos.append(NodoArbol(self, inicio, longitud, inicio_inicial))


class ArbolDeSufijos:
    def __init__(self, texto):
        self.texto = texto
        self.arbol = self._construir_arbol(self.texto)

    @staticmethod
    def _construir_arbol(texto):
        ultima_posicion = len(texto) - 1

        raiz = NodoArbol(None, None, None, None)

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
                            nodo_dividido = NodoArbol(nodo_actual, hijo.inicio, j, None)
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
                    nodo_actual.agregar_hijo(posicion_interna, ultima_posicion - posicion_interna + 1, posicion)
                    posicion_interna = ultima_posicion + 1

            posicion += 1

        return raiz

    def encontrar_subcadena_corta_unica(self, n, texto1):
        min_subcadena = None
        limite_texto1 = n

        nodos = []
        cola = deque([self.arbol])
        while cola:
            actual = cola.popleft()
            nodos.append(actual)
            for hijo in actual.hijos:
                cola.append(hijo)

        for nodo in reversed(nodos):
            if nodo.hijos:
                tipo_primero = False
                tipo_segundo = False
                for hijo in nodo.hijos:
                    if hijo.tipo_texto == "12" or (tipo_primero and tipo_segundo):
                        nodo.tipo_texto = "12"
                        break
                    if hijo.tipo_texto == "1":
                        tipo_primero = True
                    else:
                        tipo_segundo = True

                if nodo.tipo_texto is None:
                    if tipo_primero and tipo_segundo:
                        nodo.tipo_texto = "12"
                    elif tipo_primero:
                        nodo.tipo_texto = "1"
                    else:
                        nodo.tipo_texto = "2"
            else:
                if nodo.inicio > limite_texto1:
                    nodo.tipo_texto = "2"
                else:
                    nodo.tipo_texto = "1"

        cola = deque(self.arbol.hijos)
        while cola:
            actual = cola.popleft()

            if actual.tipo_texto == "12":
                for hijo in actual.hijos:
                    cola.append(hijo)
            elif actual.tipo_texto == "1":
                fin = min(actual.inicio + 1, limite_texto1)
                candidata = texto1[actual.inicio:fin]
                if candidata != "":
                    while actual.padre.padre is not None:
                        actual = actual.padre
                        fin = actual.inicio + actual.longitud
                        candidata = texto1[actual.inicio:fin] + candidata

                    if min_subcadena is None or len(candidata) < len(min_subcadena):
                        min_subcadena = candidata

        return min_subcadena

def ejecutar_algoritmo():
    texto1 = sys.stdin.readline().strip()
    texto2 = sys.stdin.readline().strip()
    n = len(texto1)
    s = "{}#{}$".format(texto1, texto2)
    arbol = ArbolDeSufijos(s)
    resultado = arbol.encontrar_subcadena_corta_unica(n, texto1)
    print(resultado)


if __name__ == "__main__":
    ejecutar_algoritmo()
