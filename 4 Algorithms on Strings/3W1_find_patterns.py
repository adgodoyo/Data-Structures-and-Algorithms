# python3
import sys


class KnuthMorrisPratt:
    def __init__(self, texto, patron):
        self.texto = texto
        self.patron = patron
        self.inicios_patron = self._obtener_inicios_patron(self.texto, self.patron)

    def _obtener_inicios_patron(self, texto, patron):
        s = "".join([patron, "$", texto])
        arreglo_prefijo = self._obtener_arreglo_prefijo(s)

        resultado = []
        for i in range(len(patron) + 1, len(s)):
            if arreglo_prefijo[i] == len(patron):
                posicion_inicio = i - 2 * len(patron)
                resultado.append(posicion_inicio)

        return resultado

    @staticmethod
    def _obtener_arreglo_prefijo(s):
        resultado = [0]
        borde = 0

        for i in range(1, len(s)):
            while (borde > 0) and (s[i] != s[borde]):
                borde = resultado[borde - 1]

            if s[i] == s[borde]:
                borde += 1
            else:
                borde = 0

            resultado.append(borde)

        return resultado

def ejecutar_algoritmo():
    patron = sys.stdin.readline().strip()
    texto = sys.stdin.readline().strip()
    kmp = KnuthMorrisPratt(texto, patron)
    resultado = kmp.inicios_patron
    print(" ".join(map(str, resultado)))


if __name__ == "__main__":
    ejecutar_algoritmo()
