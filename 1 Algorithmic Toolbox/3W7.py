def largest_number(numbers):
    from functools import cmp_to_key

    def compare(x, y):
        if x + y > y + x:
            return -1
        elif x + y < y + x:
            return 1
        else:
            return 0

    numbers = list(map(str, numbers))

    sorted_numbers = sorted(numbers, key=cmp_to_key(compare))

    return ''.join(sorted_numbers)


if __name__ == '__main__':
    _ = int(input())
    input_numbers = list(map(int, input().split()))
    print(largest_number(input_numbers))
