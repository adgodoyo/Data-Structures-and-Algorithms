# python3
import sys
from functools import lru_cache


class Solucionador:
    multiplicador = 1234
    primo = 1000000009

    def __init__(self, texto, patron, num_diferencias):
        self.t = texto
        self.p = patron
        self.k = num_diferencias
        self.longitud = len(self.p)

        self.hashes_t = self._precomputar_hashes(self.t, self.primo)
        self.hashes_p = self._precomputar_hashes(self.p, self.primo)

    def _precomputar_hashes(self, cadena, primo):
        hashes = [0 for _ in range(len(cadena) + 1)]
        for i in range(1, len(cadena) + 1):
            hashes[i] = (
                self.multiplicador * hashes[i - 1]
                + ord(cadena[i - 1])
            ) % primo
        return hashes

    @staticmethod
    def _exponenciacion_modular(a, b, n):
        d = 1
        b = str(bin(b))[2:]
        for i in range(len(b)):
            d = (d * d) % n
            if int(b[i]) == 1:
                d = (d * a) % n
        return d

    @lru_cache(maxsize=1024*4)
    def _calcular_hash_subcadena(self, tipo_hash, primo, inicio, longitud):
        if tipo_hash == "t":
            hashes = self.hashes_t
        else:
            hashes = self.hashes_p

        y = self._exponenciacion_modular(self.multiplicador, longitud, primo)
        hash_subcadena = (hashes[inicio + longitud] - y * hashes[inicio]) % primo
        return hash_subcadena

    def resolver(self):
        resultado = []

        for i in range(len(self.t) - self.longitud + 1):
            diferencias_actuales = 0
            a = i
            base_b = i + self.longitud - 1
            b = base_b
            while diferencias_actuales <= self.k:
                desajuste = -1
                while a <= b:
                    mitad = (a + b) // 2

                    hash_t = self._calcular_hash_subcadena("t", self.primo, a, mitad-a+1)
                    hash_p = self._calcular_hash_subcadena("p", self.primo, a-i, mitad-a+1)

                    if hash_t == hash_p:
                        a = mitad + 1
                    else:
                        desajuste = mitad
                        b = mitad - 1

                if desajuste != -1:
                    diferencias_actuales += 1
                    a = desajuste + 1
                    b = base_b
                else:
                    resultado.append(i)
                    break
        return resultado

    def resolver_naive(self):
        resultado = []

        for i in range(len(self.t) - self.longitud + 1):
            diferencias = 0
            for j in range(self.longitud):
                if self.t[i + j] != self.p[j]:
                    diferencias += 1

            if diferencias > self.k:
                continue
            resultado.append(i)

        return resultado


def ejecutar_algoritmo():
    for linea in sys.stdin.readlines():
        num_diferencias, texto, patron = linea.split()
        respuesta = Solucionador(texto, patron, int(num_diferencias)).resolver()
        print(len(respuesta), *respuesta)


if __name__ == "__main__":
    ejecutar_algoritmo()
