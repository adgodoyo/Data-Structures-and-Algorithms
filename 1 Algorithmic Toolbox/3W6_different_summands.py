def optimal_summands(n):
    summands = []
    current = 1

    while n > 0:
        if n - current > current:
            summands.append(current)
            n -= current
        else:
            summands.append(n)
            break
        current += 1

    return summands


if __name__ == '__main__':
    n = int(input())
    summands = optimal_summands(n)
    print(len(summands))
    print(*summands)
