def compute_operations(n):
    # Arreglo para almacenar el número mínimo de operaciones para cada número
    min_operations = [0] * (n + 1)
    # Arreglo para rastrear el camino de las operaciones
    prev = [0] * (n + 1)

    # Calcular el número mínimo de operaciones para cada número hasta n
    for i in range(2, n + 1):
        # Opción 1: Restar 1
        min_ops = min_operations[i - 1] + 1
        prev[i] = i - 1

        # Opción 2: Dividir entre 2
        if i % 2 == 0 and min_operations[i // 2] + 1 < min_ops:
            min_ops = min_operations[i // 2] + 1
            prev[i] = i // 2

        # Opción 3: Dividir entre 3
        if i % 3 == 0 and min_operations[i // 3] + 1 < min_ops:
            min_ops = min_operations[i // 3] + 1
            prev[i] = i // 3

        min_operations[i] = min_ops

    # Reconstruir la secuencia de operaciones
    sequence = []
    current = n
    while current > 0:
        sequence.append(current)
        current = prev[current]

    return sequence[::-1]


if __name__ == '__main__':
    input_n = int(input())
    output_sequence = compute_operations(input_n)
    print(len(output_sequence) - 1)
    print(*output_sequence)
