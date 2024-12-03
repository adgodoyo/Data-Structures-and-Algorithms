# python 3
class TamañoÓptimoKMer:
    def __init__(self, lecturas):
        self.lecturas = lecturas

    def resolver(self):
        k_min = 3
        k_max = len(self.lecturas[0])

        while k_min <= k_max:
            k = (k_min + k_max) // 2

            k_mers = set()
            for lectura in self.lecturas:
                for i in range(len(lectura) - k + 1):
                    k_mers.add("".join(lectura)[i:(i + k)])
            k_mers = tuple(k_mers)

            k_menos_1_mers = set()
            for k_mer in k_mers:
                k_menos_1_mers.add(k_mer[:-1])
                k_menos_1_mers.add(k_mer[1:])
            k_menos_1_mers = tuple(k_menos_1_mers)

            aristas = self.grafo_de_bruijn(k_mers, k_menos_1_mers)

            if not self.existe_ciclo(len(k_menos_1_mers), aristas):
                k_max = k - 1
            else:
                k_min = k + 1
        return k_max

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

    @staticmethod
    def existe_ciclo(n, aristas):
        grado_entrada = [0] * n
        grado_salida = [0] * n

        for v1, v2 in aristas:
            grado_salida[v1] += 1
            grado_entrada[v2] += 1

        ciclo = True
        for g1, g2 in zip(grado_entrada, grado_salida):
            if g1 != g2:
                ciclo = False
                break
        return ciclo


def ejecutar_prueba():
    lecturas = ("AACG", "ACGT", "CAAC", "GTTG", "TGCA")
    k = TamañoÓptimoKMer(lecturas).resolver()
    print(k)


def ejecutar_algoritmo():
    n_lecturas = 400
    lecturas = []
    for _ in range(n_lecturas):
        lecturas.append(input().strip())
    lecturas = tuple(lecturas)

    k = TamañoÓptimoKMer(lecturas).resolver()
    print(k)


if __name__ == "__main__":
    ejecutar_algoritmo()
