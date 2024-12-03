# python3
from itertools import combinations


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
                return []

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


class ProblemaDieta:
    INFINITO = 10**9

    def __init__(self, n, m, A, b, c):
        self.n = n
        self._n = self.n + 1
        self.m = m
        self.A = A
        self._A = self.A.copy()
        self._A.append([1 for _ in range(self.m)])
        self.b = b
        self._b = self.b.copy()
        self._b.append(self.INFINITO)
        self.c = c

    def resolver(self):
        combinaciones_ecuaciones = combinations(range(self._n + self.m), self.m)

        resultados = []
        for ecuaciones in combinaciones_ecuaciones:
            matriz = []
            ecuacion_inf = False
            for i in ecuaciones:
                if i < self._n:
                    fila = list(self._A[i])
                    fila.append(self._b[i])
                else:
                    fila = [0 for _ in range(self.m + 1)]
                    fila[i - self._n] = 1
                matriz.append(fila)

                if i == self.n:
                    ecuacion_inf = True

            mg = MetodoGauss(matriz)
            solucion = mg.resolver()
            if not solucion:
                continue

            violada = False
            i = 0
            while not violada and (i < self.n):
                resultado = sum(map(lambda x: x[0] * x[1], zip(self._A[i], solucion)))
                if round(resultado, 2) > self._b[i]:
                    violada = True
                i += 1
            i = 0
            while not violada and (i < self.m):
                if round(solucion[i], 2) < 0:
                    violada = True
                i += 1

            if not violada:
                resultados.append((solucion, ecuacion_inf))

        if not resultados:
            respuesta = "No solution"
        else:
            max_resultado = None
            max_valor = -self.INFINITO
            inf_max_resultado = False
            for resultado, ecuacion_inf in resultados:
                valor = sum(map(lambda x: x[0] * x[1], zip(resultado, self.c)))
                valor = round(valor, 2)
                if valor > max_valor:
                    max_valor = valor
                    max_resultado = resultado
                    inf_max_resultado = ecuacion_inf
                if (valor == max_valor) and not ecuacion_inf:
                    max_resultado = resultado
                    inf_max_resultado = False

            if inf_max_resultado:
                respuesta = "Infinity"
            else:
                respuesta = "Bounded solution\n"
                respuesta += " ".join(list(map(lambda x: "%.18f" % x, max_resultado)))
        return respuesta

def algoritmo():
    n, m = list(map(int, input().split()))
    A = []
    for i in range(n):
        A.append(list(map(int, input().split())))
    b = list(map(int, input().split()))
    c = list(map(int, input().split()))

    pd = ProblemaDieta(n, m, A, b, c)
    respuesta = pd.resolver()
    print(respuesta)


if __name__ == "__main__":
    algoritmo()
