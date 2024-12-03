from sys import stdin


def points_cover_optimized(starts, ends, points):
    events = []
    result = {}

    # Agregar los eventos de inicio, fin y los puntos
    for start in starts:
        events.append((start, 'L'))
    for end in ends:
        events.append((end, 'R'))
    for index, point in enumerate(points):
        events.append((point, 'P', index))

    # Ordenar eventos: primero por coordenada, luego 'L' < 'P' < 'R'
    events.sort(key=lambda x: (x[0], x[1]))

    active_segments = 0

    for event in events:
        if event[1] == 'L':
            active_segments += 1
        elif event[1] == 'R':
            active_segments -= 1
        else:  # Evento de punto
            _, _, index = event
            result[index] = active_segments

    # Ordenar los resultados por el índice original de los puntos
    return [result[i] for i in range(len(points))]


if __name__ == '__main__':
    data = list(map(int, stdin.read().split()))
    n, m = data[0], data[1]
    input_starts, input_ends = data[2:2 * n + 2:2], data[3:2 * n + 2:2]
    input_points = data[2 * n + 2:]

    output_count = points_cover_optimized(input_starts, input_ends, input_points)
    print(*output_count)
