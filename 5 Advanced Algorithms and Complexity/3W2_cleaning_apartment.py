# python3
from collections import defaultdict


class CaminoHamiltonianoASAT:
    def __init__(self, num_vertices, aristas):
        self.num_vertices = num_vertices
        self.aristas = aristas

    def _pertenece_a_un_camino(self):
        sat = []
        for v in range(1, self.num_vertices + 1):
            clausula = tuple(range(
                (v - 1) * self.num_vertices + 1,
                (v - 1) * self.num_vertices + self.num_vertices + 1
            ))
            sat.append(clausula)
        return sat

    def _una_vez_en_un_camino(self):
        sat = []
        for v in range(1, self.num_vertices + 1):
            for pos1 in range(1, self.num_vertices):
                for pos2 in range(pos1 + 1, self.num_vertices + 1):
                    x1 = -(self.num_vertices * (v - 1) + pos1)
                    x2 = -(self.num_vertices * (v - 1) + pos2)
                    sat.append((x1, x2))
        return sat

    def _cada_pos_por_algún_vertice(self):
        sat = []
        for pos in range(1, self.num_vertices + 1):
            clausula = tuple(range(pos, self.num_vertices**2 + 1, self.num_vertices))
            sat.append(clausula)
        return sat

    def _no_dos_vertices_misma_pos(self):
        sat = []
        for pos in range(1, self.num_vertices + 1):
            for v1 in range(1, self.num_vertices):
                for v2 in range(v1 + 1, self.num_vertices + 1):
                    x1 = -(self.num_vertices * (v1 - 1) + pos)
                    x2 = -(self.num_vertices * (v2 - 1) + pos)
                    sat.append((x1, x2))
        return sat

    def _conectados_por_una_arista(self):
        lista_adyacencia = defaultdict(set)
        for v1, v2 in self.aristas:
            lista_adyacencia[v1].add(v2)
            lista_adyacencia[v2].add(v1)

        sat = []
        for v1 in range(1, self.num_vertices):
            for v2 in range(v1 + 1, self.num_vertices + 1):
                if v2 not in lista_adyacencia[v1]:
                    for pos in range(1, self.num_vertices):
                        x1 = -((v1 - 1) * self.num_vertices + pos)
                        x2 = -((v2 - 1) * self.num_vertices + (pos + 1) % (self.num_vertices + 1))
                        sat.append((x1, x2))

                        x1 = -((v2 - 1) * self.num_vertices + pos)
                        x2 = -((v1 - 1) * self.num_vertices + (pos + 1) % (self.num_vertices + 1))
                        sat.append((x1, x2))
        return sat

    def convertir(self):
        sat = []
        sat.extend(self._pertenece_a_un_camino())
        sat.extend(self._una_vez_en_un_camino())
        sat.extend(self._cada_pos_por_algún_vertice())
        sat.extend(self._no_dos_vertices_misma_pos())
        sat.extend(self._conectados_por_una_arista())
        return sat


def algoritmo():
    num_vertices, num_aristas = map(int, input().split())
    aristas = [list(map(int, input().split())) for _ in range(num_aristas)]
    ch_a_sat = CaminoHamiltonianoASAT(num_vertices, aristas)
    sat = ch_a_sat.convertir()
    print(len(sat), num_vertices**2)
    for clausula in sat:
        s = " ".join(map(str, clausula))
        s += " 0"
        print(s)


if __name__ == "__main__":
    algoritmo()
