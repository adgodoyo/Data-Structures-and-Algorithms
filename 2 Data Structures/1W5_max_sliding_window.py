from collections import deque

def max_sliding_window(sequence, m):
    dq = deque()
    maximums = []

    for i in range(len(sequence)):
        # Remover elementos fuera de la ventana
        if dq and dq[0] < i - m + 1:
            dq.popleft()

        # Remover elementos menores al actual, ya que no serán necesarios
        while dq and sequence[dq[-1]] < sequence[i]:
            dq.pop()

        # Agregar el índice actual
        dq.append(i)

        # El máximo de la ventana actual es el elemento en la cabeza del deque
        if i >= m - 1:
            maximums.append(sequence[dq[0]])

    return maximums


if __name__ == '__main__':
    n = int(input())
    input_sequence = [int(i) for i in input().split()]
    assert len(input_sequence) == n
    window_size = int(input())

    print(*max_sliding_window(input_sequence, window_size))
