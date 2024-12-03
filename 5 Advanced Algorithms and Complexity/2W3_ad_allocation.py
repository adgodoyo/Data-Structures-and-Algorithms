# python3
from itertools import combinations
from time import sleep

DEBUG = False


class AsignacionAnuncios:
    def __init__(self, A, b, c):
        self.A = A
        self.b = b
        self.c = c

    def resolver(self):
        n = len(self.A)
        m = len(self.A[0])
        signos = ["<=" for _ in range(n)]
        x_no_negativas = [True for _ in range(m)]
        maximizar = True
        algoritmo = SIMPLEX(n, m, self.A, signos, self.b, x_no_negativas, self.c, maximizar)
        resultado = algoritmo.resolver()
        if resultado[1] == "No solution":
            print("No solution")
        elif resultado[1] == "Infinity":
            print("Infinity")
        else:
            print("Bounded solution")
            print(" ".join(map(str, resultado[0][1])))


class SIMPLEX:
    EPS = 0.00001

    def __init__(self, n, m, A, signos, b, x_no_negativas, c, maximizar=True):
        self.n = n
        self.m = m
        self.A = A
        self.signos = signos
        self.b = b
        self.x_no_negativas = x_no_negativas
        self.c = c
        self.maximizar = maximizar

    def resolver(self):
        resultado = None

        A, b, c = self._a_forma_estandar(
            self.A,
            self.signos,
            self.b,
            self.x_no_negativas,
            self.c,
            self.maximizar
        )
        self.imprimir_forma_estandar(A, b, c)

        A, b, c, N, B, v, msg = self._init_simplex(A, b, c)

        if msg == "No solution":
            return resultado, msg

        while True:
            if DEBUG:
                self.imprimir_forma_canonica(A, b, c, N, B, v)

            variable_entrante = self._obtener_variable_entrante(c, N)
            if variable_entrante is None:
                x = [0 for _ in range(len(A) + len(A[0]))]
                for i, j in enumerate(B):
                    x[j] = b[i]

                resultado = (v, x[:len(A[0])])
                msg = "Bounded solution"
                break

            if DEBUG:
                print("Entrante: {}".format(variable_entrante + 1))

            variable_saliente = self._obtener_variable_saliente(A, b, N, B, variable_entrante)
            if variable_saliente is None:
                resultado = float("inf")
                msg = "Infinity"
                break
            if DEBUG:
                print("Saliente: {}".format(variable_saliente + 1))

            A, b, c, v, N, B = self._pivotar(A, b, c, v, N, B, variable_saliente, variable_entrante)

            if DEBUG:
                sleep(0.1)

        return resultado, msg

    @staticmethod
    def imprimir_forma_estandar(A, b, c):
        if DEBUG:
            print()
        msg_objetivo = "maximize "
        for i, c_i in enumerate(c):
            if i > 0:
                if c_i >= 0:
                    msg_objetivo += " + "
                else:
                    msg_objetivo += " - "
                    c_i *= -1
            msg_objetivo += "{}*x{}".format(c_i, i + 1)
        if DEBUG:
            print(msg_objetivo)

        for i, fila in enumerate(A):
            msg_fila = ""
            for j, x_i in enumerate(fila):
                if j > 0:
                    if x_i >= 0:
                        msg_fila += " + "
                    else:
                        msg_fila += " - "
                        x_i *= -1
                msg_fila += "{}*x{}".format(x_i, j + 1)
            msg_fila += " <= "
            msg_fila += "{}".format(b[i])
            if DEBUG:
                print(msg_fila)

    @staticmethod
    def _a_forma_estandar(A, signos, b, x_no_negativas, c, maximizar):
        A = A.copy()
        b = b.copy()
        c = c.copy()

        if not maximizar:
            c = [x * (-1) for x in c]

        desplazamiento = 0
        for i, no_negativa in enumerate(x_no_negativas):
            if not no_negativa:
                j = i + desplazamiento
                desplazamiento += 1
                for k, fila in enumerate(A):
                    A[k] = fila[:(j + 1)] + [(-1) * fila[j]] + fila[(j + 1):]
                c = c[:(j + 1)] + [(-1) * c[j]] + c[(j + 1):]

        signos_, A_, b_ = [], [], []
        for i, signo in enumerate(signos):
            if signo == "=":
                signos_.append("<=")
                A_.append(A[i])
                b_.append(b[i])
                signos_.append(">=")
                A_.append([(-1) * x for x in A[i]])
                b_.append((-1) * b[i])
            else:
                signos_.append(signo)
                A_.append(A[i])
                b_.append(b[i])
        signos = signos_
        A = A_
        b = b_

        for i, signo in enumerate(signos):
            if signo == ">=":
                A[i] = [(-1) * x for x in A[i]]
                b[i] *= -1

        return A, b, c

    @staticmethod
    def _obtener_variable_entrante(c, N):
        var = None
        min_i = max(N) + 1
        for i, coef in enumerate(c):
            if (coef > 0) and (N[i] < min_i):
                var = N[i]
                min_i = N[i]
        return var

    @staticmethod
    def _obtener_variable_saliente(A, b, N, B, e):
        e_i = N.index(e)
        var = None
        delta = []
        for i, fila in enumerate(A):
            coef = fila[e_i]
            if coef > 0:
                delta.append(b[i] / coef)
            else:
                delta.append(float("inf"))

        min_i = max(B) + 1
        min_delta = float("inf")
        for i, d in enumerate(delta):
            if (d < float("inf")) and (d <= min_delta):
                if d < min_delta:
                    min_delta = d
                    min_i = B[i]
                else:
                    if B[i] < min_i:
                        min_delta = d
                        min_i = B[i]
        if min_delta < float("inf"):
            var = min_i
        return var

    @staticmethod
    def _pivotar(A, b, c, v, N, B, l, e):
        fila_saliente = B.index(l)
        columna_entrante = N.index(e)
        coef = A[fila_saliente][columna_entrante]
        A[fila_saliente][columna_entrante] = 1
        A[fila_saliente] = [x / coef for x in A[fila_saliente]]
        b[fila_saliente] /= coef
        for i in range(len(A)):
            if i == fila_saliente:
                continue
            coef = A[i][columna_entrante]
            b[i] = b[i] - coef * b[fila_saliente]
            for j in range(len(A[0])):
                A[i][j] = A[i][j] - coef * A[fila_saliente][j]
            A[i][columna_entrante] = -1 * coef * A[fila_saliente][columna_entrante]
        coef = c[columna_entrante]
        v += coef * b[fila_saliente]
        for j in range(len(c)):
            c[j] = c[j] - coef * A[fila_saliente][j]
        c[columna_entrante] = -1 * coef * A[fila_saliente][columna_entrante]
        B[fila_saliente] = e
        N[columna_entrante] = l
        return A, b, c, v, N, B


def algoritmo():
    n, m = list(map(int, input().split()))
    A = []
    for i in range(n):
        A += [list(map(int, input().split()))]
    b = list(map(int, input().split()))
    c = list(map(int, input().split()))
    aa = AsignacionAnuncios(A, b, c)
    aa.resolver()


if __name__ == "__main__":
    algoritmo()
