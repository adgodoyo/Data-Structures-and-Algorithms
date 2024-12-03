from sys import stdin

def optimal_value(capacity, weights, values):
    value = 0.0
    value_per_weight = [(v / w, w) for v, w in zip(values, weights)]
    value_per_weight.sort(reverse=True, key=lambda x: x[0])  # Ordenar por valor por peso en orden descendente

    for v_w, weight in value_per_weight:
        if capacity == 0:
            break
        amount = min(weight, capacity)  # Tomar el peso que se pueda (o lo que queda del espacio en la mochila)
        value += amount * v_w  # Agregar valor proporcional
        capacity -= amount  # Reducir capacidad disponible

    return value


if __name__ == "__main__":
    data = list(map(int, stdin.read().split()))
    n, capacity = data[0:2]
    values = data[2:(2 * n + 2):2]
    weights = data[3:(2 * n + 2):2]
    opt_value = optimal_value(capacity, weights, values)
    print("{:.10f}".format(opt_value))

