# python3
import random


class GrafoImplicaciones:
    def __init__(self, n_variables, clausulas):
        self.n_variables = n_variables
        self.clausulas = clausulas
        self._n = self.n_variables * 2
        self.id_interno, self.id_original = self._obtener_mapeos_ids(self.n_variables)
        self._lista_adyacencia, self._lista_adyacencia_r = self._construir_listas_adyacencia()

    @staticmethod
    def _obtener_mapeos_ids(n_variables):
        id_interno = dict()
        id_original = [0 for _ in range(n_variables * 2)]
        for i in range(1, n_variables + 1):
            id_positivo = n_variables + i - 1
            id_negativo = n_variables - i
            id_interno[i] = id_positivo
            id_interno[-i] = id_negativo
            id_original[id_positivo] = i
            id_original[id_negativo] = -i
        return id_interno, id_original

    def _construir_listas_adyacencia(self):
        lista_adyacencia = [set() for _ in range(self._n)]
        lista_adyacencia_r = [set() for _ in range(self._n)]
        for x, y in self.clausulas:
            id_x = self.id_interno[x]
            id_no_x = self.id_interno[-x]
            id_y = self.id_interno[y]
            id_no_y = self.id_interno[-y]
            lista_adyacencia[id_no_x].add(id_y)
            lista_adyacencia[id_no_y].add(id_x)
            lista_adyacencia_r[id_y].add(id_no_x)
            lista_adyacencia_r[id_x].add(id_no_y)
        return lista_adyacencia, lista_adyacencia_r

    def explorar_vertice(self, v, visitados, lista_adyacencia, postorden):
        visitados[v] = True
        for hijo in lista_adyacencia[v]:
            if not visitados[hijo]:
                self.explorar_vertice(hijo, visitados, lista_adyacencia, postorden)
        postorden.append(v)

    def dfs(self, lista_adyacencia):
        visitados = [False] * len(lista_adyacencia)
        postorden = []
        for v in range(len(lista_adyacencia)):
            if not visitados[v]:
                stack = [v]
                while stack:
                    actual = stack[-1]
                    sin_hijos = True
                    for hijo in lista_adyacencia[actual]:
                        if not visitados[hijo]:
                            stack.append(hijo)
                            visitados[hijo] = True
                            sin_hijos = False
                            break
                    if sin_hijos:
                        stack.pop()
                        postorden.append(actual)
        return postorden

    def encontrar_sccs(self):
        postorden_r = self.dfs(self._lista_adyacencia_r)
        visitados = [False] * self._n
        sccs = []
        id_sccs = [-1 for _ in range(self._n)]
        id_actual = 0
        for v in reversed(postorden_r):
            if not visitados[v]:
                explorados = self.explorar_scc(v, visitados, self._lista_adyacencia)
                sccs.append(explorados)
                for e in explorados:
                    id_sccs[e] = id_actual
                id_actual += 1
        return sccs, id_sccs

    def explorar_scc(self, v, visitados, lista_adyacencia):
        explorados = set()
        stack = [v]
        while stack:
            actual = stack.pop()
            if not visitados[actual]:
                visitados[actual] = True
                explorados.add(actual)
                for hijo in lista_adyacencia[actual]:
                    if not visitados[hijo]:
                        stack.append(hijo)
        return explorados

    def es_insatisfacible(self, id_sccs):
        insatisfacible = False
        for x in range(1, self.n_variables + 1):
            id_x = id_sccs[self.id_interno[x]]
            id_no_x = id_sccs[self.id_interno[-x]]
            if id_x == id_no_x:
                insatisfacible = True
                break
        return insatisfacible


class DosSAT:
    def __init__(self, n_variables, clausulas):
        self.n_variables = n_variables
        self.clausulas = clausulas

    def es_satisfacible(self):
        grafo = GrafoImplicaciones(self.n_variables, self.clausulas)
        sccs, id_sccs = grafo.encontrar_sccs()
        if grafo.es_insatisfacible(id_sccs):
            return None
        asignacion = [None] * self.n_variables
        for scc in reversed(sccs):
            for x in scc:
                variable = grafo.id_original[x]
                indice = abs(variable) - 1
                if asignacion[indice] is None:
                    asignacion[indice] = variable > 0
        return asignacion


class TresRecoloreos:
    def __init__(self, n_vertices, aristas, colores, bucle_vertice):
        self.n = n_vertices
        self.aristas = aristas
        self.colores = colores
        self.bucle_vertice = bucle_vertice

    def resolver(self):
        if self.bucle_vertice:
            return "Imposible"
        clausulas = self._construir_clausulas()
        dos_sat = DosSAT(self.n * 2, clausulas)
        resultado = dos_sat.es_satisfacible()
        if resultado is None:
            return "Imposible"
        solucion = []
        for i in range(self.n):
            color_actual = self.colores[i]
            nuevo_color = "GB" if resultado[2 * i] else "RG"
            solucion.append(nuevo_color[0] if color_actual == "R" else nuevo_color[1])
        return "".join(solucion)

    def _construir_clausulas(self):
        clausulas = []
        for i in range(self.n):
            col1 = 2 * i + 1
            col2 = col1 + 1
            clausulas.append([col1, col2])
            clausulas.append([-col1, -col2])
        for v1, v2 in self.aristas:
            col1_v1, col2_v1 = 2 * (v1 - 1) + 1, 2 * (v1 - 1) + 2
            col1_v2, col2_v2 = 2 * (v2 - 1) + 1, 2 * (v2 - 1) + 2
            clausulas.append([-col1_v1, -col1_v2])
            clausulas.append([-col2_v1, -col2_v2])
        return clausulas


def ejecutar_prueba():
    n_vertices = 3
    colores = "RBG"
    aristas = [[1, 3], [2, 1]]
    tres_recoloreos = TresRecoloreos(n_vertices, aristas, colores, False)
    print(tres_recoloreos.resolver())


if __name__ == "__main__":
    ejecutar_prueba()
