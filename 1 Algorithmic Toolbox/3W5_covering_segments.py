from sys import stdin
from collections import namedtuple

Segment = namedtuple('Segment', 'start end')

def optimal_points(segments):
    points = []

    # Ordenar los segmentos por el punto de finalización en orden ascendente
    segments.sort(key=lambda s: s.end)

    # Mientras queden segmentos, seleccionamos el punto más a la derecha
    while segments:
        # Seleccionamos el final del primer segmento
        current_point = segments[0].end
        points.append(current_point)

        # Eliminamos todos los segmentos que contienen este punto
        segments = [s for s in segments if s.start > current_point]

    return points


if __name__ == '__main__':
    input = stdin.read()
    n, *data = map(int, input.split())
    segments = list(map(lambda x: Segment(x[0], x[1]), zip(data[::2], data[1::2])))
    points = optimal_points(segments)
    print(len(points))
    print(*points)
