import sys

class StackWithMax():
    def __init__(self):
        self.__stack = []
        self.__max_stack = []

    def Push(self, a):
        self.__stack.append(a)
        # Actualizar la pila de máximos
        if not self.__max_stack or a >= self.__max_stack[-1]:
            self.__max_stack.append(a)

    def Pop(self):
        assert(len(self.__stack))
        value = self.__stack.pop()
        # Actualizar la pila de máximos si el elemento eliminado era el máximo
        if value == self.__max_stack[-1]:
            self.__max_stack.pop()

    def Max(self):
        assert(len(self.__stack))
        return self.__max_stack[-1]


if __name__ == '__main__':
    stack = StackWithMax()

    num_queries = int(sys.stdin.readline())
    for _ in range(num_queries):
        query = sys.stdin.readline().split()

        if query[0] == "push":
            stack.Push(int(query[1]))
        elif query[0] == "pop":
            stack.Pop()
        elif query[0] == "max":
            print(stack.Max())
        else:
            assert(0)
