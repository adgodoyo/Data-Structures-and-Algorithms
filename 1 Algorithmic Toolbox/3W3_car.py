from sys import stdin


def min_refills(distance, tank, stops):
    # Agregar la posición inicial (0) y la posición final (distance) a las paradas
    stops = [0] + stops + [distance]
    num_refills = 0
    current_position = 0
    last_refill = 0

    while current_position < len(stops) - 1:
        last_refill = current_position

        # Avanzar lo más lejos posible dentro del alcance del tanque
        while (current_position < len(stops) - 1 and
               stops[current_position + 1] - stops[last_refill] <= tank):
            current_position += 1

        # Si no se avanzó, no es posible llegar al destino
        if current_position == last_refill:
            return -1

        # Si no estamos en la última parada, incrementamos el número de recargas
        if current_position < len(stops) - 1:
            num_refills += 1

    return num_refills


if __name__ == '__main__':
    d, m, _, *stops = map(int, stdin.read().split())
    print(min_refills(d, m, stops))
