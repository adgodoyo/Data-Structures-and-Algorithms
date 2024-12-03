# python 3
from collections import deque, defaultdict


class CicloEuleriano:
    def __init__(self, n, aristas):
        self.n = n
        self.aristas = aristas
        self.m = len(self.aristas)

    def encontrar_camino(self):
        camino = None

        if not self.existe_ciclo():
            return camino

        lista_adyacencia = [[] for _ in range(self.n)]
        for i, arista in enumerate(self.aristas):
            v_inicio = arista[0]
            lista_adyacencia[v_inicio].append(i)

        m_explorado = 0
        arista_explorada = [False] * self.m
        vertice_no_explorado = 0
        ciclos = []

        while m_explorado < self.m:
            for i in range(vertice_no_explorado, self.n):
                if lista_adyacencia[i]:
                    id_arista = lista_adyacencia[i].pop()
                    arista_explorada[id_arista] = True
                    m_explorado += 1
                    vertice_no_explorado = i
                    break

            v_inicio, v_siguiente = self.aristas[id_arista]
            ciclo = [v_inicio, v_siguiente]
            while v_siguiente != v_inicio:
                id_arista = lista_adyacencia[v_siguiente].pop()
                arista_explorada[id_arista] = True
                m_explorado += 1
                v_siguiente = self.aristas[id_arista][1]
                ciclo.append(v_siguiente)
            ciclos.append(ciclo)

        inicio_ciclos = defaultdict(list)
        for i, ciclo in enumerate(ciclos):
            inicio_ciclos[ciclo[0]].append(i)

        camino = []
        pila_camino = deque([ciclos[0][0]])

        while pila_camino:
            vertice_actual = pila_camino.popleft()
            if (vertice_actual in inicio_ciclos) and inicio_ciclos[vertice_actual]:
                id_ciclo = inicio_ciclos[vertice_actual].pop()
                for v in ciclos[id_ciclo][1:][::-1]:
                    pila_camino.appendleft(v)
            camino.append(vertice_actual)
        return camino

    def existe_ciclo(self):
        grado_entrada = [0] * self.n
        grado_salida = [0] * self.n

        for v1, v2 in self.aristas:
            grado_salida[v1] += 1
            grado_entrada[v2] += 1

        ciclo = True
        for g1, g2 in zip(grado_entrada, grado_salida):
            if g1 != g2:
                ciclo = False
                break
        return ciclo


class CadenaBinariaKUniversal:
    def __init__(self, k):
        self.k = k

    def resolver(self):
        k_mers = []
        for i in range(2 ** self.k):
            s = format(i, "0{}b".format(self.k))
            k_mers.append(s)

        k_menos_1_mers = []
        for i in range(2 ** (self.k - 1)):
            s = format(i, "0{}b".format(self.k - 1))
            k_menos_1_mers.append(s)

        aristas = self.grafo_de_bruijn(k_mers, k_menos_1_mers)

        ce = CicloEuleriano(len(k_menos_1_mers), aristas)
        camino = ce.encontrar_camino()

        subcadenas = [k_menos_1_mers[camino[0]][-1:]]
        for i in camino[1:-1]:
            subcadenas.append(k_menos_1_mers[i][-1:])
        s = "".join(subcadenas)
        return s

    def grafo_de_bruijn(self, k_mers, k_menos_1_mers):
        mapa_k_menos_1_mer_a_id = dict()
        for i, k_mer in enumerate(k_menos_1_mers):
            mapa_k_menos_1_mer_a_id[k_mer] = i

        aristas = set()
        for k_mer in k_mers:
            v1 = mapa_k_menos_1_mer_a_id[k_mer[:-1]]
            v2 = mapa_k_menos_1_mer_a_id[k_mer[1:]]
            aristas.add((v1, v2))
        aristas = tuple(aristas)
        return aristas

def ejecutar_algoritmo():
    k = int(input())
    resultado = CadenaBinariaKUniversal(k).resolver()
    print(resultado)


if __name__ == "__main__":
    ejecutar_algoritmo()
