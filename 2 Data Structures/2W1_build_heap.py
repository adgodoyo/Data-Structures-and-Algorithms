def build_heap(data):
    """Build a heap from `data` inplace using the sift-down operation.

    Returns a sequence of swaps performed by the algorithm.
    """
    swaps = []

    def sift_down(i):
        """Ensure the subtree rooted at index `i` satisfies the heap property."""
        min_index = i
        left = 2 * i + 1
        right = 2 * i + 2

      
        if left < len(data) and data[left] < data[min_index]:
            min_index = left

 
        if right < len(data) and data[right] < data[min_index]:
            min_index = right

        if i != min_index:
            swaps.append((i, min_index))
            data[i], data[min_index] = data[min_index], data[i]
            sift_down(min_index)

    for i in range(len(data) // 2 - 1, -1, -1):
        sift_down(i)

    return swaps


def main():
    n = int(input())
    data = list(map(int, input().split()))
    assert len(data) == n

    swaps = build_heap(data)

    print(len(swaps))
    for i, j in swaps:
        print(i, j)


if __name__ == "__main__":
    main()
