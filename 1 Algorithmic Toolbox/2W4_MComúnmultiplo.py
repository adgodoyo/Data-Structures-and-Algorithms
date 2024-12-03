def mcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def mcm(a, b):
    return abs(a * b) // mcd(a, b)

if __name__ == '__main__':
    a, b = map(int, input().split())
    print(mcm(a, b))

