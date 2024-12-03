# python3
import sys
from collections import defaultdict


class InverseBWT:
    def __init__(self, bwt):
        self.bwt = bwt
        self.texto = self._calcular_texto(self.bwt)

    @staticmethod
    def _calcular_texto(bwt):
        ultima_columna = bwt
        primera_columna = "".join(sorted(bwt))

        primer_caracter_a_conteo = []
        contador_primera = defaultdict(int)

        ultimo_caracter_a_conteo = []
        contador_ultima = defaultdict(int)

        for i in range(len(bwt)):
            primer_caracter_a_conteo.append(contador_primera[primera_columna[i]])
            contador_primera[primera_columna[i]] += 1

            ultimo_caracter_a_conteo.append(contador_ultima[ultima_columna[i]])
            contador_ultima[ultima_columna[i]] += 1

        ultimo_caracter_id_a_id = dict()
        for i in range(len(bwt)):
            ultimo_caracter_id_a_id[(ultima_columna[i], ultimo_caracter_a_conteo[i])] = i

        s = ""
        i = 0
        for _ in range(len(bwt)):
            i = ultimo_caracter_id_a_id[(primera_columna[i], primer_caracter_a_conteo[i])]
            s += primera_columna[i]

        return s


def ejecutar_algoritmo():
    bwt = sys.stdin.readline().strip()
    ibwt = InverseBWT(bwt)
    print(ibwt.texto)


if __name__ == "__main__":
    ejecutar_algoritmo()
