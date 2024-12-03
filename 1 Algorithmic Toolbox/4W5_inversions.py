def merge_and_count(arr, temp_arr, left, mid, right):
    i = left    # Índice para la sublista izquierda
    j = mid + 1 # Índice para la sublista derecha
    k = left    # Índice para el arreglo temporal
    inv_count = 0

    # Combina las dos sublistas mientras cuentas las inversiones
    while i <= mid and j <= right:
        if arr[i] <= arr[j]:
            temp_arr[k] = arr[i]
            i += 1
        else:
            temp_arr[k] = arr[j]
            inv_count += (mid - i + 1)  # Todos los elementos restantes en la sublista izquierda son inversiones
            j += 1
        k += 1

    # Copia los elementos restantes de la sublista izquierda
    while i <= mid:
        temp_arr[k] = arr[i]
        i += 1
        k += 1

    # Copia los elementos restantes de la sublista derecha
    while j <= right:
        temp_arr[k] = arr[j]
        j += 1
        k += 1

    # Copia los elementos ordenados de temp_arr a arr
    for i in range(left, right + 1):
        arr[i] = temp_arr[i]

    return inv_count


def merge_sort_and_count(arr, temp_arr, left, right):
    inv_count = 0
    if left < right:
        mid = (left + right) // 2

        inv_count += merge_sort_and_count(arr, temp_arr, left, mid)
        inv_count += merge_sort_and_count(arr, temp_arr, mid + 1, right)
        inv_count += merge_and_count(arr, temp_arr, left, mid, right)

    return inv_count


def count_inversions(arr):
    temp_arr = [0] * len(arr)
    return merge_sort_and_count(arr, temp_arr, 0, len(arr) - 1)


if __name__ == '__main__':
    input_n = int(input())
    elements = list(map(int, input().split()))
    assert len(elements) == input_n
    print(count_inversions(elements))
