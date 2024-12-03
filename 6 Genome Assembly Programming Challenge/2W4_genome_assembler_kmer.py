# python 3
from collections import deque


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
            ciclo = [v_inicio]
            while v_siguiente != v_inicio:
                ciclo.append(v_siguiente)
                id_arista = lista_adyacencia[v_siguiente].pop()
                arista_explorada[id_arista] = True
                m_explorado += 1
                v_siguiente = self.aristas[id_arista][1]
            ciclos.append(ciclo)

        ciclos_conjuntos = []
        for i, ciclo in enumerate(ciclos):
            ciclos_conjuntos.append(set(ciclo))
            ciclos[i] = deque(ciclo)

        ciclos_visitados = [False] * len(ciclos)

        camino = []
        pila_camino = deque(list(ciclos[0]))
        ciclos_visitados[0] = True

        while pila_camino:
            vertice_actual = pila_camino.popleft()
            for i, conjunto_ciclo in enumerate(ciclos_conjuntos):
                if ciclos_visitados[i]:
                    continue

                if vertice_actual in conjunto_ciclo:
                    while ciclos[i][-1] != vertice_actual:
                        ciclos[i].rotate(1)

                    for v in reversed(ciclos[i]):
                        pila_camino.appendleft(v)

                    ciclos_visitados[i] = True
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


class CadenaUniversal:
    def __init__(self, patrones):
        self.patrones = patrones
        self.k = len(self.patrones[0])

    def resolver(self):
        k_mers = self.patrones

        k_menos_1_mers = set()
        for k_mer in k_mers:
            k_menos_1_mers.add(k_mer[:-1])
            k_menos_1_mers.add(k_mer[1:])
        k_menos_1_mers = tuple(k_menos_1_mers)

        aristas = self.grafo_de_bruijn(k_mers, k_menos_1_mers)

        ce = CicloEuleriano(len(k_menos_1_mers), aristas)
        camino = ce.encontrar_camino()

        subcadenas = []
        for i in camino:
            subcadenas.append(k_menos_1_mers[i][-1:])
        s = "".join(subcadenas)
        return s

    @staticmethod
    def grafo_de_bruijn(k_mers, k_menos_1_mers):
        mapa_k_menos_1_mer_a_id = dict()
        for i, k_mer in enumerate(k_menos_1_mers):
            mapa_k_menos_1_mer_a_id[k_mer] = i

        aristas = []
        for k_mer in k_mers:
            v1 = mapa_k_menos_1_mer_a_id[k_mer[:-1]]
            v2 = mapa_k_menos_1_mer_a_id[k_mer[1:]]
            aristas.append((v1, v2))
        aristas = tuple(aristas)
        return aristas


class EnsambladorGenomaKmer:
    def __init__(self, k_mers):
        self.k_mers = k_mers

    def resolver(self):
        s = CadenaUniversal(self.k_mers).resolver()
        return s


def ejecutar_algoritmo():
    n_kmers = 5396
    k_mers = []
    for _ in range(n_kmers):
        k_mer = input().strip()
        k_mers.append(k_mer)
    k_mers = tuple(k_mers)

    resultado = EnsambladorGenomaKmer(k_mers).resolver()
    print(resultado)


if __name__ == "__main__":
    ejecutar_algoritmo()
