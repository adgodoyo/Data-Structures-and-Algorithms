# python 3

from collections import defaultdict


class DeteccionBurbujas:
    def __init__(self, k, umbral, lecturas):
        self.k = k
        self.umbral = umbral
        self.lecturas = lecturas

        self._adj_list_cnt = None
        self._en_pila = None

    def contar_burbujas(self):
        k_mers = self.obtener_k_mers()
        k_menos_1_mers = self.obtener_k_menos_1_mers(k_mers)

        n = len(k_menos_1_mers)
        aristas = self.grafo_de_bruijn(k_mers, k_menos_1_mers)
        lista_adyacencia = self.aristas_a_lista_adyacencia(n, aristas)

        num_burbujas = 0
        for v_inicio in range(n):
            caminos_crudos = self.dfs_caminos_umbral(v_inicio, lista_adyacencia, self.umbral)

            caminos = defaultdict(list)
            for camino in caminos_crudos:
                caminos[camino[-1]].append(camino)

            for v_fin, caminos_actual in caminos.items():
                if len(caminos_actual) <= 1:
                    continue

                for i in range(len(caminos_actual) - 1):
                    camino_i_interno = set(caminos_actual[i][1:-1])
                    for j in range(i, len(caminos_actual)):
                        camino_j_interno = set(caminos_actual[j][1:-1])
                        if len(camino_i_interno.intersection(camino_j_interno)) == 0:
                            num_burbujas += 1
        return num_burbujas

    def dfs_caminos_umbral(self, v_inicio, lista_adyacencia, umbral):
        if self._adj_list_cnt is None:
            self._adj_list_cnt = [0] * len(lista_adyacencia)
        if self._en_pila is None:
            self._en_pila = [False] * len(lista_adyacencia)

        caminos = set()
        pila = [v_inicio]
        self._en_pila[v_inicio] = True

        while pila:
            if len(pila) > 1:
                caminos.add(tuple(pila))

            v_ultimo = pila[-1]
            adj_list_i = self._adj_list_cnt[v_ultimo]
            while adj_list_i < len(lista_adyacencia[v_ultimo]):
                v_siguiente = lista_adyacencia[v_ultimo][adj_list_i]
                adj_list_i += 1
                if not self._en_pila[v_siguiente]:
                    self._adj_list_cnt[v_ultimo] = adj_list_i
                    pila.append(v_siguiente)
                    self._en_pila[v_siguiente] = True
                    break
            else:
                pila.pop()
                self._en_pila[v_ultimo] = False
                self._adj_list_cnt[v_ultimo] = 0

            if len(pila) == (umbral + 1):
                caminos.add(tuple(pila))
                v_ultimo = pila.pop()
                self._en_pila[v_ultimo] = False
                self._adj_list_cnt[v_ultimo] = 0
        return caminos

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
    def aristas_a_lista_adyacencia(n, aristas):
        lista_adyacencia = [[] for _ in range(n)]
        for v1, v2 in aristas:
            lista_adyacencia[v1].append(v2)
        return lista_adyacencia

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
    k, umbral = map(int, input().split())
    lecturas = []
    for _ in range(1618):
        lecturas.append(input().strip())

    bd = DeteccionBurbujas(k, umbral, lecturas)
    print(bd.contar_burbujas())


if __name__ == "__main__":
    ejecutar_algoritmo()
