import sys
from collections import namedtuple
import random

Prueba = namedtuple("Prueba", "s t salida")
Respuesta = namedtuple("tipo_respuesta", "i j longitud")


class Solucionador:
    _multiplicador = 1234
    _primo1 = 87178291199
    _primo2 = 3314192745739

    def __init__(self, cadena1, cadena2):
        self.cadena1 = cadena1
        self.cadena2 = cadena2

        self.longitud_maxima = min(len(self.cadena1), len(self.cadena2))

        self.hashes_cadena1_1 = self._precomputar_hashes(self.cadena1, self._primo1)
        self.hashes_cadena1_2 = self._precomputar_hashes(self.cadena1, self._primo2)

        self.hashes_cadena2_1 = self._precomputar_hashes(self.cadena2, self._primo1)
        self.hashes_cadena2_2 = self._precomputar_hashes(self.cadena2, self._primo2)

    def _precomputar_hashes(self, cadena, primo):
        hashes = [0 for _ in range(len(cadena) + 1)]
        for i in range(1, len(cadena) + 1):
            hashes[i] = (
                self._multiplicador * hashes[i - 1]
                + ord(cadena[i - 1])
            ) % primo
        return hashes

    def _precomputar_hashes_subcadenas(self, hashes, longitud, primo):
        hashes_subcadenas = dict()
        for i in range(len(hashes) - longitud):
            hashes_subcadenas[self._calcular_hash_subcadena(hashes, primo, i, longitud)] = i
        return hashes_subcadenas

    @staticmethod
    def _exponenciacion_modular(a, b, n):
        d = 1
        b = str(bin(b))[2:]
        for i in range(len(b)):
            d = (d * d) % n
            if int(b[i]) == 1:
                d = (d * a) % n
        return d

    def _calcular_hash_subcadena(self, hashes, primo, inicio, longitud):
        y = self._exponenciacion_modular(self._multiplicador, longitud, primo)
        hash_subcadena = (hashes[inicio + longitud] - y * hashes[inicio]) % primo
        return hash_subcadena

    def subcadena_comun_mas_larga(self):
        respuesta = Respuesta(0, 0, 0)

        a = 1
        b = self.longitud_maxima

        while a <= b:
            longitud = (a + b) // 2
            encontrado = False

            hashes_c1_1 = self._precomputar_hashes_subcadenas(self.hashes_cadena1_1, longitud, self._primo1)
            hashes_c2_1 = self._precomputar_hashes_subcadenas(self.hashes_cadena2_1, longitud, self._primo1)

            hashes_comunes1 = set(hashes_c1_1).intersection(hashes_c2_1)

            if hashes_comunes1:
                ind = hashes_comunes1.pop()
                i = hashes_c1_1[ind]
                j = hashes_c2_1[ind]

                hash_c1_2 = self._calcular_hash_subcadena(self.hashes_cadena1_2, self._primo2, i, longitud)
                hash_c2_2 = self._calcular_hash_subcadena(self.hashes_cadena2_2, self._primo2, j, longitud)

                if hash_c1_2 == hash_c2_2 and (longitud > respuesta.longitud):
                    respuesta = Respuesta(i, j, longitud)
                    encontrado = True

            if encontrado:
                a = longitud + 1
            else:
                b = longitud - 1

        return respuesta


def resolver_naive(cadena1, cadena2):
    respuesta = Respuesta(0, 0, 0)
    for i in range(len(cadena1)):
        for j in range(len(cadena2)):
            for longitud in range(min(len(cadena1) - i, len(cadena2) - j) + 1):
                if (longitud > respuesta.longitud) and (cadena1[i:i + longitud] == cadena2[j:j + longitud]):
                    respuesta = Respuesta(i, j, longitud)
    return respuesta

def ejecutar_algoritmo():
    for linea in sys.stdin.readlines():
        cadena1, cadena2 = linea.split()
        respuesta = Solucionador(cadena1, cadena2).subcadena_comun_mas_larga()
        print(respuesta.i, respuesta.j, respuesta.longitud)


if __name__ == "__main__":
    ejecutar_algoritmo()

