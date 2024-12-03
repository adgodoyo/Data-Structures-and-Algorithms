# python 3

from collections import deque, defaultdict


class CicloEuleriano:
    def __init__(self, n, aristas):
        self.n = n
        self.aristas = aristas
        self.m = len(self.aristas)

    def encontrar_ciclo(self):
        ciclo = None

        if not self.existe_ciclo():
            return ciclo

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
            ciclo_actual = [v_inicio, v_siguiente]
            while v_siguiente != v_inicio:
                id_arista = lista_adyacencia[v_siguiente].pop()
                arista_explorada[id_arista] = True
                m_explorado += 1
                v_siguiente = self.aristas[id_arista][1]
                ciclo_actual.append(v_siguiente)
            ciclos.append(ciclo_actual)

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

def ejecutar_algoritmo():
    num_vertices, num_aristas = map(int, input().split())

    aristas = []
    for _ in range(num_aristas):
        v1, v2 = map(int, input().split())
        v1, v2 = v1 - 1, v2 - 1
        aristas.append((v1, v2))

    ce = CicloEuleriano(num_vertices, aristas)
    camino = ce.encontrar_ciclo()

    if camino is None:
        print(0)
    else:
        print(1)
        print(" ".join(map(lambda x: str(x + 1), camino[:-1])))


if __name__ == "__main__":
    ejecutar_algoritmo()
