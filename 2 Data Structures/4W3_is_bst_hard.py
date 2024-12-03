class TreeNode:
    def __init__(self, val, min_val=float('-inf'), max_val=float('inf')):
        self.val = val
        self.min = min_val
        self.max = max_val
        self.left = None
        self.right = None

    def __repr__(self):
        return str(self.val)


class Solution:
    # Método iterativo para verificar si el árbol es un BST
    def isBST(self, root):
        if not root:
            return True

        stack = [root]
        while stack:
            node = stack.pop()
            if node.min > node.val or node.val >= node.max:
                return False

            if node.right:
                node.right.min = node.val
                node.right.max = node.max
                stack.append(node.right)

            if node.left:
                node.left.min = node.min
                node.left.max = node.val
                stack.append(node.left)

        return True


def main():
    # Leer el número de nodos
    N = int(input().strip())

    if N == 0:
        print("CORRECT")
        return

    # Crear nodos y asignarlos a una lista
    nodes = [TreeNode(0) for _ in range(N)]

    # Leer las conexiones de los nodos
    for i in range(N):
        val, L, R = map(int, input().split())
        nodes[i].val = val
        if L != -1:
            nodes[i].left = nodes[L]
        if R != -1:
            nodes[i].right = nodes[R]

    # Comprobar si el árbol es un BST
    solution = Solution()
    result = solution.isBST(nodes[0])
    print("CORRECT" if result else "INCORRECT")


if __name__ == "__main__":
    main()
