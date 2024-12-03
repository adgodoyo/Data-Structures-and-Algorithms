# python3
from itertools import starmap
from operator import mul


class ProgramacionEnteraLinealASAT:
    sol1 = (
        (0,),
        (1,),
    )
    sol2 = (
        (0, 0),
        (0, 1),
        (1, 0),
        (1, 1),
    )
    sol3 = (
        (0, 0, 0),
        (0, 0, 1),
        (0, 1, 0),
        (0, 1, 1),
        (1, 0, 0),
        (1, 0, 1),
        (1, 1, 0),
        (1, 1, 1),
    )

    def __init__(self, A, b):
        self.A = A
        self.b = b

    def _desigualdad_a_sat(self, fila, valor):
        ids_no_cero, elementos_no_cero = [], []
        for i, a in enumerate(fila):
            if a != 0:
                ids_no_cero.append(i + 1)
                elementos_no_cero.append(a)
                if len(elementos_no_cero) == 3:
                    break

        num_elementos_no_cero = len(elementos_no_cero)
        sat = []
        if num_elementos_no_cero == 0:
            return sat

        if num_elementos_no_cero == 1:
            soluciones = self.sol1
        elif num_elementos_no_cero == 2:
            soluciones = self.sol2
        else:
            soluciones = self.sol3

        for s in soluciones:
            resultado = sum(starmap(mul, zip(elementos_no_cero, s)))
            if resultado > valor:
                signos = [1 if x == 0 else -1 for x in s]
                clausula = tuple(starmap(mul, zip(signos, ids_no_cero)))
                sat.append(clausula)
        return sat

    def convertir(self):
        sat = []
        for i in range(len(self.A)):
            fila = self.A[i]
            valor = self.b[i]
            sat_fila = self._desigualdad_a_sat(fila, valor)
            if sat_fila:
                sat.extend(sat_fila)

        if not sat:
            sat.append((1, -1))
        return sat

def algoritmo():
    num_desigualdades, num_variables = list(map(int, input().split()))
    A = []
    for _ in range(num_desigualdades):
        A += [list(map(int, input().split()))]
    b = list(map(int, input().split()))

    pel_a_sat = ProgramacionEnteraLinealASAT(A, b)
    sat = pel_a_sat.convertir()

    print(len(sat), num_variables)
    for clausula in sat:
        s = " ".join(map(str, clausula))
        s += " 0"
        print(s)


if __name__ == "__main__":
    algoritmo()
