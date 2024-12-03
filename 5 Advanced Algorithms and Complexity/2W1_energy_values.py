# python3
class MetodoGauss:
    def __init__(self, matriz):
        self.matriz = matriz
        self.n = len(self.matriz)

    def resolver(self):
        for i in range(self.n):
            for k in range(i, self.n):
                if self.matriz[k][i] != 0:
                    actual = k
                    break
            else:
                return "Multiple solutions!"

            if actual != i:
                self.matriz[i], self.matriz[actual] = self.matriz[actual], self.matriz[i]

            coef = self.matriz[i][i]
            for j in range(i, self.n + 1):
                self.matriz[i][j] /= coef

            for k in range(i + 1, self.n):
                coef = self.matriz[k][i]
                for j in range(i, self.n + 1):
                    self.matriz[k][j] -= coef * self.matriz[i][j]

        for i in range(self.n - 1, -1, -1):
            for j in range(i - 1, -1, -1):
                coef = self.matriz[j][i]
                self.matriz[j][i] -= coef * self.matriz[i][i]
                self.matriz[j][self.n] -= coef * self.matriz[i][self.n]

        resultado = [self.matriz[i][-1] for i in range(self.n)]
        return resultado

    def imprimir(self):
        print("Matrix:")
        for fila in self.matriz:
            print(fila)
        print()

def algoritmo():
    tamano = int(input())
    matriz = []
    for _ in range(tamano):
        fila = list(map(float, input().split()))
        matriz.append(fila)

    mg = MetodoGauss(matriz)
    resultado = mg.resolver()
    print(" ".join(map(lambda x: str(round(x, 4)), resultado)))


if __name__ == "__main__":
    algoritmo()
