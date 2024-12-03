# python 3

from collections import defaultdict


class EnsambladorGenoma:
    LONGITUD_CADENA = 100
    NUM_ERRORES_CADENA = 2

    def __init__(self, dataset):
        self.dataset = self.eliminar_duplicados(dataset)
        self.n = len(self.dataset)

    def eliminar_duplicados(self, dataset):
        n = len(dataset)
        duplicado = [False] * n

        for i in range(n - 1):
            if duplicado[i]:
                continue

            s1 = dataset[i]
            for j in range(i + 1, n):
                if duplicado[j]:
                    continue

                s2 = dataset[j]

                if self.tiene_menos_errores(s1, s2, max_errores=EnsambladorGenoma.NUM_ERRORES_CADENA):
                    duplicado[j] = True

        dataset_filtrado = []
        for i in range(n):
            if not duplicado[i]:
                dataset_filtrado.append(dataset[i])
        return dataset_filtrado

    @staticmethod
    def tiene_menos_errores(s1, s2, max_errores=2):
        errores = 0
        resultado = True
        for i in range(EnsambladorGenoma.LONGITUD_CADENA):
            if s1[i] != s2[i]:
                errores += 1
            if errores > max_errores:
                resultado = False
                break
        return resultado

    def resolver(self):
        procesado = [False] * self.n
        solape = [0] * self.n
        siguiente_id = [0] * self.n

        i = 0
        for _ in range(self.n - 1):
            s1 = self.dataset[i]
            procesado[i] = True
            for j in range(1, self.n):
                if procesado[j]:
                    continue

                s2 = self.dataset[j]

                nuevo_solape = self.encontrar_solape_mayor(s1, s2, solape[i])

                if nuevo_solape is not None:
                    siguiente_id[i] = j
                    solape[i] = nuevo_solape

            i = siguiente_id[i]

        siguiente_id[i] = 0
        solape[i] = self.encontrar_solape_mayor(self.dataset[i], self.dataset[0])
        ultimo_solape = solape[i]

        posicion_inicio = 0
        cadenas_con_errores = [(0, posicion_inicio)]
        actual = 0
        for _ in range(self.n - 1):
            posicion_inicio += EnsambladorGenoma.LONGITUD_CADENA - solape[actual]
            cadenas_con_errores.append((siguiente_id[actual], posicion_inicio))
            actual = siguiente_id[actual]

        longitud_total = posicion_inicio + EnsambladorGenoma.LONGITUD_CADENA

        for _ in range(self.n - 1, self.n * 2):
            posicion_inicio += EnsambladorGenoma.LONGITUD_CADENA - solape[actual]
            cadenas_con_errores.append((siguiente_id[actual], posicion_inicio))
            actual = siguiente_id[actual]

        caracteres = []
        for i in range(longitud_total):
            contador = defaultdict(int)
            for id_cadena, posicion_inicio in cadenas_con_errores:
                if posicion_inicio <= i < (posicion_inicio + EnsambladorGenoma.LONGITUD_CADENA):
                    contador[self.dataset[id_cadena][i - posicion_inicio]] += 1

            max_frecuencia = 0
            char = ""
            for c, frecuencia in contador.items():
                if frecuencia > max_frecuencia:
                    char = c
                    max_frecuencia = frecuencia
            caracteres.append(char)

        resultado = "".join(caracteres)
        resultado = resultado[ultimo_solape:]
        return resultado

    @staticmethod
    def encontrar_solape_mayor(s1, s2, solape_prev=0):
        resultado = None
        for solape in range(EnsambladorGenoma.LONGITUD_CADENA - 1, solape_prev, -1):
            errores = 0
            inicio_s1 = EnsambladorGenoma.LONGITUD_CADENA - solape
            for i in range(solape):
                if s1[inicio_s1 + i] != s2[i]:
                    errores += 1
                    if errores > EnsambladorGenoma.NUM_ERRORES_CADENA:
                        break
            else:
                resultado = solape
                break
        return resultado


def ejecutar_algoritmo():
    filas = 1618
    dataset = [input().strip()]
    for _ in range(filas - 1):
        dataset.append(input().strip())

    ensamblador = EnsambladorGenoma(dataset)
    respuesta = ensamblador.resolver()
    print(respuesta)


if __name__ == "__main__":
    ejecutar_algoritmo()
