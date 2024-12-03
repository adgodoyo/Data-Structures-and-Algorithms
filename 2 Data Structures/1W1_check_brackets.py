from collections import namedtuple

Bracket = namedtuple("Bracket", ["char", "position"])


def are_matching(left, right):
    return (left + right) in ["()", "[]", "{}"]


def find_mismatch(text):
    opening_brackets_stack = []

    for i, next in enumerate(text):
        if next in "([{":
            # Agregar el bracket y su posición a la pila
            opening_brackets_stack.append(Bracket(next, i + 1))

        if next in ")]}":
            # Si la pila está vacía, significa que hay un bracket de cierre no emparejado
            if not opening_brackets_stack:
                return i + 1

            # Verificar si el bracket actual cierra correctamente el último bracket de apertura
            top = opening_brackets_stack.pop()
            if not are_matching(top.char, next):
                return i + 1

    # Verificar si quedan brackets de apertura sin cerrar
    if opening_brackets_stack:
        return opening_brackets_stack[0].position

    return "Success"


def main():
    text = input()
    mismatch = find_mismatch(text)
    print(mismatch)


if __name__ == "__main__":
    main()
