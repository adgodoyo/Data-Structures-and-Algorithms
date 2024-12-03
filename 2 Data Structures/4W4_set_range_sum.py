from sys import stdin

MODULO = 1000000001


class Nodo:
    def __init__(self, clave, suma_subarbol=0, izquierdo=None, derecho=None, padre=None):
        self.clave = clave
        self.suma_subarbol = suma_subarbol
        self.izquierdo = izquierdo
        self.derecho = derecho
        self.padre = padre


class ArbolSplay:
    ULTIMO_RESULTADO_SUMA = 0

    def __init__(self, raiz=None):
        self.raiz = None
        if raiz is not None:
            self.raiz = raiz

    @staticmethod
    def actualizar(nodo):
        if nodo is None:
            return

        nodo.suma_subarbol = nodo.clave
        if nodo.izquierdo is not None:
            nodo.suma_subarbol += nodo.izquierdo.suma_subarbol
            nodo.izquierdo.padre = nodo
        if nodo.derecho is not None:
            nodo.suma_subarbol += nodo.derecho.suma_subarbol
            nodo.derecho.padre = nodo

    def rotacion_pequena(self, nodo):
        padre = nodo.padre

        if padre is None:
            return

        abuelo = nodo.padre.padre

        if padre.izquierdo == nodo:
            m = nodo.derecho
            nodo.derecho = padre
            padre.izquierdo = m
        else:
            m = nodo.izquierdo
            nodo.izquierdo = padre
            padre.derecho = m

        self.actualizar(padre)
        self.actualizar(nodo)

        nodo.padre = abuelo

        if abuelo is not None:
            if abuelo.izquierdo == padre:
                abuelo.izquierdo = nodo
            else:
                abuelo.derecho = nodo

    def rotacion_grande(self, nodo):
        if (nodo.padre.izquierdo == nodo) and (nodo.padre.padre.izquierdo == nodo.padre):
            self.rotacion_pequena(nodo.padre)
            self.rotacion_pequena(nodo)
        elif (nodo.padre.derecho == nodo) and (nodo.padre.padre.derecho == nodo.padre):
            self.rotacion_pequena(nodo.padre)
            self.rotacion_pequena(nodo)
        else:
            self.rotacion_pequena(nodo)
            self.rotacion_pequena(nodo)

    def splay(self, nodo):
        if nodo is None:
            return

        while nodo.padre is not None:
            if nodo.padre.padre is None:
                self.rotacion_pequena(nodo)
                break
            self.rotacion_grande(nodo)

        self.raiz = nodo
        self.raiz.padre = None

    def insertar(self, clave):
        nuevo_nodo = Nodo(clave, clave)

        if self.raiz is None:
            self.raiz = nuevo_nodo
            return

        ultimo_nodo_visitado, _ = self.buscar(clave)
        if ultimo_nodo_visitado.clave == clave:
            return

        nodo = self.raiz
        while nodo is not None:
            if clave < nodo.clave:
                if nodo.izquierdo is None:
                    nodo.izquierdo = nuevo_nodo
                    nuevo_nodo.padre = nodo
                    break
                else:
                    nodo = nodo.izquierdo
            else:
                if nodo.derecho is None:
                    nodo.derecho = nuevo_nodo
                    nuevo_nodo.padre = nodo
                    break
                else:
                    nodo = nodo.derecho

        self.splay(nuevo_nodo)

    def buscar(self, clave):
        if self.raiz is None:
            return None

        nodo = self.raiz
        ultimo_nodo_visitado = nodo
        nodo_menor_mayor = None

        while nodo is not None:
            ultimo_nodo_visitado = nodo

            if (nodo.clave <= clave) and \
                    ((nodo_menor_mayor is None) or (nodo.clave > nodo_menor_mayor.clave)):
                nodo_menor_mayor = nodo

            if nodo.clave == clave:
                break
            if nodo.clave > clave:
                nodo = nodo.izquierdo
            else:
                nodo = nodo.derecho

        if nodo_menor_mayor is not None:
            self.splay(nodo_menor_mayor)
        else:
            self.splay(ultimo_nodo_visitado)

        return ultimo_nodo_visitado, nodo_menor_mayor

    def dividir(self, clave):
        ultimo_nodo_visitado, nodo_menor_mayor = self.buscar(clave)
        if nodo_menor_mayor is not None:
            hijo_derecho = nodo_menor_mayor.derecho

            izquierdo = ArbolSplay(raiz=nodo_menor_mayor)
            if izquierdo.raiz is not None:
                izquierdo.raiz.derecho = None
                self.actualizar(izquierdo.raiz)

            derecho = ArbolSplay(raiz=hijo_derecho)
            if derecho.raiz is not None:
                derecho.raiz.padre = None
        else:
            izquierdo = ArbolSplay(raiz=None)
            derecho = ArbolSplay(raiz=ultimo_nodo_visitado)
            if derecho.raiz is not None:
                derecho.raiz.padre = None

        return izquierdo, derecho

    def unir(self, izquierdo, derecho):
        if (izquierdo.raiz is None) and (derecho.raiz is None):
            self.raiz = None
        elif izquierdo.raiz is None:
            self.raiz = derecho.raiz
        elif derecho.raiz is None:
            self.raiz = izquierdo.raiz
        else:
            nodo_max_izquierdo = izquierdo.raiz
            while nodo_max_izquierdo.derecho is not None:
                nodo_max_izquierdo = nodo_max_izquierdo.derecho

            izquierdo.splay(nodo_max_izquierdo)

            izquierdo.raiz.derecho = derecho.raiz

            izquierdo.actualizar(izquierdo.raiz)
            izquierdo.actualizar(izquierdo.raiz.derecho)
            self.raiz = izquierdo.raiz

    def buscar_clave(self, clave):
        if self.raiz is None:
            return False

        ultimo_nodo_visitado, _ = self.buscar(clave)
        if ultimo_nodo_visitado.clave == clave:
            return True
        return False

    def eliminar(self, clave):
        if self.raiz is None:
            return

        ultimo_nodo_visitado, _ = self.buscar(clave)
        if ultimo_nodo_visitado.clave == clave:
            izquierdo = ArbolSplay(ultimo_nodo_visitado.izquierdo)
            if izquierdo.raiz is not None:
                izquierdo.raiz.padre = None

            derecho = ArbolSplay(ultimo_nodo_visitado.derecho)
            if derecho.raiz is not None:
                derecho.raiz.padre = None

            self.unir(izquierdo, derecho)

    def suma(self, valor_min, valor_max):
        resultado = 0

        if self.raiz is not None:
            resultado = self.raiz.suma_subarbol

            izquierdo, medio = self.dividir(valor_min)
            if izquierdo.raiz is not None:
                resultado -= izquierdo.raiz.suma_subarbol
                if izquierdo.raiz.clave == valor_min:
                    resultado += izquierdo.raiz.clave
            self.unir(izquierdo, medio)

            medio, derecho = self.dividir(valor_max)
            if derecho.raiz is not None:
                resultado -= derecho.raiz.suma_subarbol
            self.unir(medio, derecho)

        return resultado

    def procesar_operacion(self, linea):
        linea = linea.split()

        if linea[0] == "+":
            x = int(linea[1])
            self.insertar((x + self.ULTIMO_RESULTADO_SUMA) % MODULO)
        elif linea[0] == "-":
            x = int(linea[1])
            self.eliminar((x + self.ULTIMO_RESULTADO_SUMA) % MODULO)
        elif linea[0] == "?":
            x = int(linea[1])
            print(
                "Found" if self.buscar_clave((x + self.ULTIMO_RESULTADO_SUMA) % MODULO)
                else "Not found"
            )
        elif linea[0] == "s":
            valor_min = int(linea[1])
            valor_max = int(linea[2])
            res = self.suma(
                (valor_min + self.ULTIMO_RESULTADO_SUMA) % MODULO,
                (valor_max + self.ULTIMO_RESULTADO_SUMA) % MODULO
            )
            print(res)
            self.ULTIMO_RESULTADO_SUMA = res % MODULO

    def recorrer_arbol(self):
        if self.raiz is None:
            return

        print("Inicio del recorrido")
        self._recorrer_arbol(self.raiz)
        print("Fin del recorrido")

    def _recorrer_arbol(self, nodo):
        if nodo is None:
            return

        self._recorrer_arbol(nodo.izquierdo)
        print(f"Nodo: clave={nodo.clave}, suma_subarbol={nodo.suma_subarbol}")
        self._recorrer_arbol(nodo.derecho)

def ejecutar_algoritmo():
    arbol = ArbolSplay()

    n = int(stdin.readline())

    for _ in range(n):
        linea = stdin.readline()
        arbol.procesar_operacion(linea)


if __name__ == "__main__":
    ejecutar_algoritmo()
