# python 3

from math import sqrt
from itertools import permutations


class EnsambladorRompecabezas:
    def __init__(self, cuadrados):
        self.cuadrados = cuadrados
        self._color_a_id, self._id_a_color = self._obtener_mapas_colores(self.cuadrados)
        self._cuadrados = self._obtener_cuadrados_internos(self.cuadrados, self._color_a_id)

    @staticmethod
    def _obtener_mapas_colores(cuadrados):
        color_a_id = dict()
        id_a_color = []

        color_a_id["black"] = 0
        id_a_color.append("black")

        i = 1
        for cuadrado in cuadrados:
            for color in cuadrado:
                if color not in color_a_id:
                    color_a_id[color] = i
                    id_a_color.append(color)
                    i += 1
        return color_a_id, id_a_color

    @staticmethod
    def _obtener_cuadrados_internos(cuadrados, color_a_id):
        cuadrados_internos = []
        for cuadrado in cuadrados:
            cuadrado_interno = tuple(color_a_id[color] for color in cuadrado)
            cuadrados_internos.append(cuadrado_interno)
        cuadrados_internos = tuple(cuadrados_internos)
        return cuadrados_internos

    @classmethod
    def leer_entrada(cls, n_cuadrados):
        cuadrados = []
        for _ in range(n_cuadrados):
            cuadrado = input().strip()
            cuadrado = cuadrado[1:-1]
            cuadrado = tuple(cuadrado.split(","))
            cuadrados.append(cuadrado)
        cuadrados = tuple(cuadrados)
        return cls(cuadrados)

    @staticmethod
    def imprimir_resultado(cuadrados):
        for fila in cuadrados:
            fila_resultado = []
            for cuadrado in fila:
                fila_resultado.append("(" + ",".join(cuadrado) + ")")
            fila_str = ";".join(fila_resultado)
            print(fila_str)

    def resolver(self):
        n = int(sqrt(len(self._cuadrados)))
        pos = [[-1] * n for _ in range(n)]
        borde_arriba = []
        borde_izquierdo = []
        borde_abajo = []
        borde_derecho = []
        cuadrados_internos = []
        for i, (c_a, c_i, c_b, c_d) in enumerate(self._cuadrados):
            if c_a == c_i == 0:
                pos[0][0] = i
                continue
            elif c_a == c_d == 0:
                pos[0][n - 1] = i
                continue
            elif c_i == c_b == 0:
                pos[n - 1][0] = i
                continue
            elif c_b == c_d == 0:
                pos[n - 1][n - 1] = i
                continue

            if (c_a == 0) and (c_i != 0) and (c_d != 0):
                borde_arriba.append(i)
                continue
            elif (c_i == 0) and (c_a != 0) and (c_b != 0):
                borde_izquierdo.append(i)
                continue
            elif (c_b == 0) and (c_i != 0) and (c_d != 0):
                borde_abajo.append(i)
                continue
            elif (c_d == 0) and (c_b != 0) and (c_a != 0):
                borde_derecho.append(i)
                continue

            cuadrados_internos.append(i)

        pos = self._encontrar_permutacion(
            pos,
            borde_arriba,
            borde_izquierdo,
            borde_abajo,
            borde_derecho,
            cuadrados_internos
        )

        pos_colores = [[""] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                id_cuadrado = pos[i][j]
                pos_colores[i][j] = self.cuadrados[id_cuadrado]
        return pos_colores

    def _encontrar_permutacion(self, pos, borde_arriba, borde_izquierdo,
                               borde_abajo, borde_derecho, cuadrados_internos):
        n = len(borde_arriba) + 2
        n_internos = len(borde_arriba)

        for arr in permutations(borde_arriba):
            for i, cuadrado in enumerate(arr):
                pos[0][i + 1] = cuadrado

            correcto = True
            for i in range(1, n):
                color_derecho = self._cuadrados[pos[0][i - 1]][3]
                color_izquierdo = self._cuadrados[pos[0][i]][1]
                if color_derecho != color_izquierdo:
                    correcto = False
                    break
            if not correcto:
                continue

            for izq in permutations(borde_izquierdo):
                for i, cuadrado in enumerate(izq):
                    pos[i + 1][0] = cuadrado

                correcto = True
                for i in range(1, n):
                    color_abajo = self._cuadrados[pos[i - 1][0]][2]
                    color_arriba = self._cuadrados[pos[i][0]][0]
                    if color_abajo != color_arriba:
                        correcto = False
                        break
                if not correcto:
                    continue

                for abajo in permutations(borde_abajo):
                    for i, cuadrado in enumerate(abajo):
                        pos[n - 1][i + 1] = cuadrado

                    correcto = True
                    for i in range(1, n):
                        color_derecho = self._cuadrados[pos[n - 1][i - 1]][3]
                        color_izquierdo = self._cuadrados[pos[n - 1][i]][1]
                        if color_derecho != color_izquierdo:
                            correcto = False
                            break
                    if not correcto:
                        continue

                    for der in permutations(borde_derecho):
                        for i, cuadrado in enumerate(der):
                            pos[i + 1][n - 1] = cuadrado

                        correcto = True
                        for i in range(1, n):
                            color_abajo = self._cuadrados[pos[i - 1][n - 1]][2]
                            color_arriba = self._cuadrados[pos[i][n - 1]][0]
                            if color_abajo != color_arriba:
                                correcto = False
                                break
                        if not correcto:
                            continue

                        for internos in permutations(cuadrados_internos):
                            for k, cuadrado in enumerate(internos):
                                i = k // n_internos
                                j = k % n_internos
                                pos[i + 1][j + 1] = cuadrado

                            correcto = True
                            for i in range(1, n):
                                for j in range(1, n):
                                    color_derecho = self._cuadrados[pos[i][j - 1]][3]
                                    color_izquierdo = self._cuadrados[pos[i][j]][1]

                                    if color_derecho != color_izquierdo:
                                        correcto = False
                                        break

                                    color_inferior = self._cuadrados[pos[i - 1][j]][2]
                                    color_superior = self._cuadrados[pos[i][j]][0]

                                    if color_inferior != color_superior:
                                        correcto = False
                                        break

                                if not correcto:
                                    break

                            if correcto:
                                return pos
        return None


def ejecutar_algoritmo():
    n_cuadrados = 25
    ensamblador = EnsambladorRompecabezas.leer_entrada(n_cuadrados)
    resultado = ensamblador.resolver()
    ensamblador.imprimir_resultado(resultado)


if __name__ == "__main__":
    ejecutar_algoritmo()
