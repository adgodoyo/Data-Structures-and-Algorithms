def majority_element(elements):
    # Algoritmo de Boyer-Moore para encontrar un candidato
    candidate, count = None, 0
    for element in elements:
        if count == 0:
            candidate = element
            count = 1
        elif element == candidate:
            count += 1
        else:
            count -= 1

    # Verificar si el candidato es realmente mayoría
    count = 0
    for element in elements:
        if element == candidate:
            count += 1

    if count > len(elements) // 2:
        return 1
    else:
        return 0


if __name__ == '__main__':
    input_n = int(input())
    input_elements = list(map(int, input().split()))
    assert len(input_elements) == input_n
    print(majority_element(input_elements))
