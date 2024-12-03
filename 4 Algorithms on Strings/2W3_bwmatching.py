# python3
import sys


class BWMatching:
    def __init__(self, bwt):
        self.bwt = bwt
        self.inicios, self.ocurrencias_antes = self._preprocesar(self.bwt)

    @staticmethod
    def _preprocesar(bwt):
        primera_columna = sorted(bwt)

        inicios = {}
        caracteres_unicos = set()

        for i in range(len(bwt)):
            char = primera_columna[i]
            if char not in inicios:
                inicios[char] = i
                caracteres_unicos.add(char)

        ocurrencias_antes = {char: [0] for char in caracteres_unicos}
        for i in range(len(bwt)):
            char_actual = bwt[i]
            for char in caracteres_unicos:
                valor = ocurrencias_antes[char][-1]
                if char == char_actual:
                    valor += 1
                ocurrencias_antes[char].append(valor)

        return inicios, ocurrencias_antes

    def contar_ocurrencias(self, patron):
 
        num_ocurrencias = 0

        top = 0
        bot = len(self.bwt) - 1
        while top <= bot:
            if len(patron):
                char = patron[-1]
                patron = patron[:-1]

                if char in self.inicios:
                    top = self.inicios[char] + self.ocurrencias_antes[char][top]
                    bot = self.inicios[char] + self.ocurrencias_antes[char][bot + 1] - 1
                else:
                    break
            else:
                num_ocurrencias = bot - top + 1
                break

        return num_ocurrencias



def ejecutar_algoritmo():
    bwt = sys.stdin.readline().strip()
    num_patrones = int(sys.stdin.readline().strip())
    patrones = sys.stdin.readline().strip().split()
    bwm = BWMatching(bwt)
    conteos_ocurrencias = []
    for patron in patrones:
        num_ocurrencias = bwm.contar_ocurrencias(patron)
        conteos_ocurrencias.append(num_ocurrencias)
    print(" ".join(map(str, conteos_ocurrencias)))


if __name__ == "__main__":
    ejecutar_algoritmo()
