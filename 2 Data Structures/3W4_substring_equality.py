# python3

import sys

class Solver:
    def __init__(self, s):
        self.s = s
        self.prime = 1000000007
        self.multiplier = 263
        self.precompute_hashes()

    def precompute_hashes(self):
        """Precomputa los hashes y las potencias del multiplicador."""
        n = len(self.s)
        self.hashes = [0] * (n + 1)
        self.powers = [1] * (n + 1)

        for i in range(1, n + 1):
            self.hashes[i] = (self.hashes[i - 1] * self.multiplier + ord(self.s[i - 1])) % self.prime
            self.powers[i] = (self.powers[i - 1] * self.multiplier) % self.prime

    def hash_substring(self, start, length):
        """Devuelve el hash de la subcadena que comienza en 'start' con longitud 'length'."""
        end = start + length
        hash_value = (self.hashes[end] - self.powers[length] * self.hashes[start]) % self.prime
        return hash_value if hash_value >= 0 else hash_value + self.prime

    def ask(self, a, b, l):
        """Compara las subcadenas s[a:a+l] y s[b:b+l] usando sus hashes."""
        hash_a = self.hash_substring(a, l)
        hash_b = self.hash_substring(b, l)
        return hash_a == hash_b


def main():
    s = sys.stdin.readline().strip()
    q = int(sys.stdin.readline())
    solver = Solver(s)

    for _ in range(q):
        a, b, l = map(int, sys.stdin.readline().split())
        print("Yes" if solver.ask(a, b, l) else "No")


if __name__ == "__main__":
    main()
