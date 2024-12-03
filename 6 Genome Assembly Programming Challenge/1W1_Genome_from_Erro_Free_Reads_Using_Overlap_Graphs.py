# python 3

class EnsambladorGenoma:
    LONGITUD_CADENA = 100

    def __init__(self, dataset):
        self.dataset = dataset
        self.n = len(self.dataset)

    def resolver(self):
        siguiente = [(0, None) for _ in range(self.n)]

        for i in range(self.n - 1):
            s1 = self.dataset[i]
            for j in range(i + 1, self.n):
                s2 = self.dataset[j]

                tamaño_solape_prev_i, _ = siguiente[i]
                tamaño_solape_prev_j, _ = siguiente[j]

                tamaño_solape_i = self.encontrar_solape_mayor(s1, s2, tamaño_solape_prev_i)
                tamaño_solape_j = self.encontrar_solape_mayor(s2, s1, tamaño_solape_prev_j)

                if tamaño_solape_i is not None:
                    siguiente[i] = (tamaño_solape_i, j)
                if tamaño_solape_j is not None:
                    siguiente[j] = (tamaño_solape_j, i)

        partes_cadena = [self.dataset[0]]
        tamaño_solape, actual = siguiente[0]
        while actual != 0:
            partes_cadena.append(self.dataset[actual][tamaño_solape:])
            tamaño_solape, actual = siguiente[actual]

        resultado = "".join(partes_cadena)
        resultado = resultado[:-tamaño_solape]
        return resultado

    @staticmethod
    def encontrar_solape_mayor(s1, s2, tamaño_solape_prev):
        resultado = None
        for tamaño_solape in range(EnsambladorGenoma.LONGITUD_CADENA - 1, tamaño_solape_prev, -1):
            if s2.startswith(s1[(EnsambladorGenoma.LONGITUD_CADENA - tamaño_solape):]):
                resultado = tamaño_solape
                break
        return resultado

def ejecutar_algoritmo():
    filas = 1618
    dataset = [input().strip()]
    for _ in range(filas - 1):
        cadena = input().strip()
        if cadena != dataset[-1]:
            dataset.append(cadena)

    ensamblador = EnsambladorGenoma(dataset)
    respuesta = ensamblador.resolver()
    print(respuesta)


if __name__ == "__main__":
    ejecutar_algoritmo()
