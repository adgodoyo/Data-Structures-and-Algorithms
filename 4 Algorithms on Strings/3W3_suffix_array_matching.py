# python3
import sys
from collections import defaultdict


class SuffixArrayMatching:
    def __init__(self, texto, alfabeto):
        self.texto = texto
        self._texto = self.texto + "$"
        self.alfabeto = "$" + alfabeto
        self.arreglo_de_sufijos = self._construir_arreglo_de_sufijos(self._texto)

    def _construir_arreglo_de_sufijos(self, texto):
        orden = self._ordenar_caracteres(texto)
        clase_equivalente = self._calcular_clase_equivalente(texto, orden)
        longitud_actual = 1

        while longitud_actual < len(texto):
            orden = self._ordenar_doblado(texto, longitud_actual, orden, clase_equivalente)
            clase_equivalente = self._actualizar_clase_equivalente(orden, clase_equivalente, longitud_actual)
            longitud_actual *= 2

        return orden

    def _ordenar_caracteres(self, texto):
        contador = defaultdict(list)
        for i, c in enumerate(texto):
            contador[c].append(i)

        orden = []
        for c in self.alfabeto:
            for i in contador[c]:
                orden.append(i)

        return orden

    def _calcular_clase_equivalente(self, texto, orden):
        clase_equivalente = [-1 for _ in range(len(texto))]
        clase_actual = 0
        char_previo = texto[orden[0]]

        for o in orden:
            char_actual = texto[o]
            if char_actual != char_previo:
                clase_actual += 1
                char_previo = char_actual
            clase_equivalente[o] = clase_actual

        return clase_equivalente

    @staticmethod
    def _ordenar_doblado(texto, longitud_actual, orden, clase_equivalente):
        inicios = [(orden[i] - longitud_actual) % len(texto) for i in range(len(texto))]
        contador = defaultdict(list)

        for i, inicio in enumerate(inicios):
            contador[clase_equivalente[inicio]].append(i)

        nuevo_orden = []
        for clase in range(len(texto)):
            if clase not in contador:
                break
            for pos in contador[clase]:
                nuevo_orden.append(inicios[pos])

        return nuevo_orden

    def _actualizar_clase_equivalente(self, orden, clase_equivalente, longitud_actual):
        nueva_clase_equivalente = [-1 for _ in range(len(orden))]
        clase_actual = 0
        nueva_clase_equivalente[orden[0]] = clase_actual

        for i in range(1, len(orden)):
            previo = orden[i - 1]
            actual = orden[i]
            mitad_previa = (previo + longitud_actual) % len(orden)
            mitad_actual = (actual + longitud_actual) % len(orden)

            if (clase_equivalente[previo] != clase_equivalente[actual]) \
                    or (clase_equivalente[mitad_previa] != clase_equivalente[mitad_actual]):
                clase_actual += 1

            nueva_clase_equivalente[actual] = clase_actual

        return nueva_clase_equivalente

    def encontrar_ocurrencias(self, patron):
        min_indice = 1
        max_indice = len(self._texto) - 1

        while min_indice < max_indice:
            mid_indice = (min_indice + max_indice) // 2
            inicio = self.arreglo_de_sufijos[mid_indice]
            long_sufijo = min(len(patron), len(self._texto) - inicio - 1)
            fin = inicio + long_sufijo
            sufijo_medio = self._texto[inicio:fin]

            if sufijo_medio < patron:
                min_indice = mid_indice + 1
            else:
                max_indice = mid_indice

        inicio = min_indice
        inicio_sufijo = self.arreglo_de_sufijos[inicio]
        long_sufijo = min(len(patron), len(self._texto) - inicio_sufijo - 1)
        fin_sufijo = inicio_sufijo + long_sufijo
        sufijo_inicio = self._texto[inicio_sufijo:fin_sufijo]

        if sufijo_inicio != patron:
            return set()

        max_indice = len(self._texto)
        while min_indice < max_indice:
            mid_indice = (min_indice + max_indice) // 2
            inicio = self.arreglo_de_sufijos[mid_indice]
            long_sufijo = min(len(patron), len(self._texto) - inicio - 1)
            fin = inicio + long_sufijo
            sufijo_medio = self._texto[inicio:fin]

            if sufijo_medio <= patron:
                min_indice = mid_indice + 1
            else:
                max_indice = mid_indice

        fin = min_indice
        return {self.arreglo_de_sufijos[i] for i in range(inicio, fin)}

def ejecutar_algoritmo():
    texto = sys.stdin.readline().strip()
    num_patrones = int(sys.stdin.readline().strip())
    patrones = sys.stdin.readline().strip().split()
    alfabeto = "ACGT"
    sa = SuffixArrayMatching(texto, alfabeto)
    ocurrencias = set()
    for patron in patrones:
        coincidencias = sa.encontrar_ocurrencias(patron)
        ocurrencias = ocurrencias.union(coincidencias)
    print(" ".join(map(str, ocurrencias)))


if __name__ == "__main__":
    ejecutar_algoritmo()
