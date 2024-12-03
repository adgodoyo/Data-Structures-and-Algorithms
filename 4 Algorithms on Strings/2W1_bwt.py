# python3
import sys


class BWT:
    def __init__(self, texto):
        self.texto = texto
        self.bwt = self._calcular_bwt(self.texto)

    @staticmethod
    def _calcular_bwt(texto):
        matriz = [texto]
        for _ in range(len(texto) - 1):
            texto = texto[-1] + texto[:-1]
            matriz.append(texto)

        matriz.sort()
        resultado = "".join([fila[-1] for fila in matriz])
        return resultado


def ejecutar_algoritmo():
    texto = sys.stdin.readline().strip()
    bwt = BWT(texto)
    print(bwt.bwt)


if __name__ == "__main__":
    ejecutar_algoritmo()
