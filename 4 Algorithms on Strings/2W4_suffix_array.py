# python3
import sys


def construir_arreglo_de_sufijos(texto):
    datos = []
    for i in range(len(texto)):
        datos.append((texto[i:], i))

    datos.sort(key=lambda x: x[0])
    resultado = [i for s, i in datos]

    return resultado



def ejecutar_algoritmo():
    texto = sys.stdin.readline().strip()
    print(" ".join(map(str, construir_arreglo_de_sufijos(texto))))


if __name__ == "__main__":
    ejecutar_algoritmo()
