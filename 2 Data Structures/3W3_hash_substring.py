# python3

def read_input():
    return (input().rstrip(), input().rstrip())

def print_occurrences(output):
    print(' '.join(map(str, output)))

def rabin_karp(pattern, text):
    p = len(pattern)
    t = len(text)
    if p > t:
        return []
    
    # Constantes para hashing
    prime = 1000000007
    multiplier = 263

    # Función para calcular el hash
    def poly_hash(s):
        h = 0
        for c in reversed(s):
            h = (h * multiplier + ord(c)) % prime
        return h

    # Precomputar los hashes de las subcadenas del texto
    result = []
    pattern_hash = poly_hash(pattern)
    text_hashes = [0] * (t - p + 1)
    last_substring = text[t - p:]
    text_hashes[-1] = poly_hash(last_substring)

    y = 1
    for i in range(p):
        y = (y * multiplier) % prime

    for i in range(t - p - 1, -1, -1):
        text_hashes[i] = (
            (multiplier * text_hashes[i + 1] + ord(text[i]) - y * ord(text[i + p])) % prime
        )

    # Comparar hashes y verificar igualdad de subcadenas
    for i in range(t - p + 1):
        if text_hashes[i] == pattern_hash and text[i:i + p] == pattern:
            result.append(i)

    return result

if __name__ == '__main__':
    pattern, text = read_input()
    print_occurrences(rabin_karp(pattern, text))
