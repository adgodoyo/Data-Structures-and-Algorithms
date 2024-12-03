# python3

class ColoreoGrafoASAT:
    def __init__(self, num_vertices, aristas):
        self.num_vertices = num_vertices
        self.aristas = aristas

    @staticmethod
    def _convertir_vertice_a_sat(v):
        id_final_v = v * 3
        ids_v = (id_final_v - 2, id_final_v - 1, id_final_v)

        sat_vertice = [
            (ids_v[0], ids_v[1], ids_v[2]),
            (-ids_v[0], -ids_v[1]),
            (-ids_v[0], -ids_v[2]),
            (-ids_v[1], -ids_v[2]),
        ]
        return sat_vertice

    @staticmethod
    def _convertir_arista_a_sat(v1, v2):
        id_final_v1 = v1 * 3
        ids_v1 = (id_final_v1 - 2, id_final_v1 - 1, id_final_v1)

        id_final_v2 = v2 * 3
        ids_v2 = (id_final_v2 - 2, id_final_v2 - 1, id_final_v2)

        sat_arista = [
            (-ids_v1[0], -ids_v2[0]),
            (-ids_v1[1], -ids_v2[1]),
            (-ids_v1[2], -ids_v2[2]),
        ]
        return sat_arista

    def convertir(self):
        sat = []

        for i in range(self.num_vertices):
            sat.extend(self._convertir_vertice_a_sat(i + 1))

        for v1, v2 in self.aristas:
            sat.extend(self._convertir_arista_a_sat(v1, v2))
        return sat


def algoritmo():
    num_vertices, num_aristas = map(int, input().split())
    aristas = [list(map(int, input().split())) for i in range(num_aristas)]
    cg_a_sat = ColoreoGrafoASAT(num_vertices, aristas)
    sat = cg_a_sat.convertir()
    print(len(sat), num_vertices * 3)
    for clausula in sat:
        s = " ".join(map(str, clausula))
        s += " 0"
        print(s)


if __name__ == "__main__":
    algoritmo()
