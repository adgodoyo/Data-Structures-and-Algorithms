# python 3

class EliminacionDeExtremos:
    def __init__(self, lecturas, k):
        self.lecturas = lecturas
        self.k = k

    def eliminar_extremos(self):
        k_mers = self.obtener_k_mers()
        k_menos_1_mers = self.obtener_k_menos_1_mers(k_mers)

        n = len(k_menos_1_mers)
        aristas = self.grafo_de_bruijn(k_mers, k_menos_1_mers)
        lista_adyacencia, lista_adyacencia_r = self.aristas_a_listas_adyacencia(n, aristas)

        num_extremos = 0
        while True:
            aristas_a_eliminar = set()
            for i, arista in enumerate(aristas):
                v1, v2 = arista
                if (len(lista_adyacencia[v2]) == 0) or (len(lista_adyacencia_r[v1]) == 0):
                    aristas_a_eliminar.add(i)

            if len(aristas_a_eliminar) == 0:
                break
            else:
                num_extremos += len(aristas_a_eliminar)
                aristas = [arista for i, arista in enumerate(aristas) if i not in aristas_a_eliminar]
                lista_adyacencia, lista_adyacencia_r = self.aristas_a_listas_adyacencia(n, aristas)
        return num_extremos

    def obtener_k_mers(self):
        k_mers = set()
        for lectura in self.lecturas:
            for i in range(len(lectura) - self.k + 1):
                k_mers.add("".join(lectura)[i:(i + self.k)])
        k_mers = tuple(k_mers)
        return k_mers

    @staticmethod
    def obtener_k_menos_1_mers(k_mers):
        k_menos_1_mers = set()
        for k_mer in k_mers:
            k_menos_1_mers.add(k_mer[:-1])
            k_menos_1_mers.add(k_mer[1:])
        k_menos_1_mers = tuple(k_menos_1_mers)
        return k_menos_1_mers

    @staticmethod
    def aristas_a_listas_adyacencia(n, aristas):
        lista_adyacencia = [[] for _ in range(n)]
        lista_adyacencia_r = [[] for _ in range(n)]
        for v1, v2 in aristas:
            lista_adyacencia[v1].append(v2)
            lista_adyacencia_r[v2].append(v1)
        return lista_adyacencia, lista_adyacencia_r

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


def ejecutar_algoritmo():
    lecturas = []
    for _ in range(1618):
        lecturas.append(input().strip())
    lecturas = tuple(lecturas)
    k = 15
    tr = EliminacionDeExtremos(lecturas, k)
    num_extremos = tr.eliminar_extremos()
    print(num_extremos)


if __name__ == "__main__":
    ejecutar_algoritmo()
