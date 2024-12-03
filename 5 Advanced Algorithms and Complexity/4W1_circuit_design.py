# python3

class GrafoImplicacion:
    def __init__(self, num_vars, clausulas):
        self.num_vars = num_vars
        self.clausulas = clausulas

        self._n = self.num_vars * 2
        self.a_id_interna, self.a_id_original = self._crear_mapas_id(self.num_vars)
        self._lista_ady, self._lista_ady_r = self._crear_listas_ady()

    @staticmethod
    def _crear_mapas_id(num_vars):
        a_id_interna = dict()
        a_id_original = [0 for _ in range(num_vars * 2)]
        for i in range(1, num_vars + 1):
            interno_i_positivo = num_vars + i - 1
            interno_i_negativo = num_vars - i

            a_id_interna[i] = interno_i_positivo
            a_id_interna[-i] = interno_i_negativo

            a_id_original[interno_i_positivo] = i
            a_id_original[interno_i_negativo] = -i
        return a_id_interna, a_id_original

    def _crear_listas_ady(self):
        lista_ady = [set() for _ in range(self._n)]
        lista_ady_r = [set() for _ in range(self._n)]

        for x, y in self.clausulas:
            x_i = self.a_id_interna[x]
            no_x_i = self.a_id_interna[-x]

            y_i = self.a_id_interna[y]
            no_y_i = self.a_id_interna[-y]

            lista_ady[no_x_i].add(y_i)
            lista_ady[no_y_i].add(x_i)

            lista_ady_r[y_i].add(no_x_i)
            lista_ady_r[x_i].add(no_y_i)
        return lista_ady, lista_ady_r

    @staticmethod
    def explorar_vertice(v, visitado, lista_ady):
        explorados = set()
        pila = [v]
        while pila:
            actual = pila.pop()
            if not visitado[actual]:
                visitado[actual] = True
                explorados.add(actual)
                for hijo in lista_ady[actual]:
                    if not visitado[hijo]:
                        pila.append(hijo)
        return explorados

    @staticmethod
    def dfs(lista_ady):
        visitado = [False] * len(lista_ady)
        postorden = []

        for v in range(len(lista_ady)):
            if not visitado[v]:
                visitado[v] = True
                pila = [v]
                while pila:
                    ultimo = pila[-1]

                    sin_hijos = True
                    for hijo in lista_ady[ultimo]:
                        if not visitado[hijo]:
                            pila.append(hijo)
                            visitado[hijo] = True
                            sin_hijos = False
                            break

                    if sin_hijos:
                        pila.pop()
                        postorden.append(ultimo)
        return postorden

    def encontrar_scc(self):
        postorden_r = self.dfs(self._lista_ady_r)

        visitado = [False] * self._n
        sccs = []
        id_sccs = [-1 for _ in range(self._n)]
        id_scc_actual = 0
        for v in reversed(postorden_r):
            if not visitado[v]:
                explorados = self.explorar_vertice(v, visitado, self._lista_ady)
                sccs.append(explorados)

                for e in explorados:
                    id_sccs[e] = id_scc_actual
                id_scc_actual += 1
        return sccs, id_sccs

    def obtener_sccs_en_orden_topologico(self, sccs, id_sccs):
        if len(sccs) <= 1:
            return sccs

        lista_ady_sccs = [set() for _ in range(len(sccs))]
        for padre, hijos in enumerate(self._lista_ady):
            id_scc_padre = id_sccs[padre]
            for hijo in hijos:
                id_scc_hijo = id_sccs[hijo]
                if id_scc_padre != id_scc_hijo:
                    lista_ady_sccs[id_scc_padre].add(id_scc_hijo)

        postorden = self.dfs(lista_ady_sccs)
        sccs = [sccs[i] for i in reversed(postorden)]
        return sccs

    def es_insatisfactible(self, id_sccs):
        insatisfactible = False
        for x in range(1, self.num_vars + 1):
            id_scc_x = id_sccs[self.a_id_interna[x]]
            id_scc_no_x = id_sccs[self.a_id_interna[-x]]
            if id_scc_x == id_scc_no_x:
                insatisfactible = True
                break
        return insatisfactible


class DosSAT:
    def __init__(self, num_vars, clausulas):
        self.num_vars = num_vars
        self.clausulas = clausulas

    def es_satisfactible(self):
        gi = GrafoImplicacion(self.num_vars, self.clausulas)
        sccs, id_sccs = gi.encontrar_scc()
        if gi.es_insatisfactible(id_sccs):
            return None
        sccs = gi.obtener_sccs_en_orden_topologico(sccs, id_sccs)

        respuesta = [None for _ in range(self.num_vars)]
        asignados = 0
        for scc in reversed(sccs):
            for x in scc:
                var = gi.a_id_original[x]
                i = abs(var) - 1
                if respuesta[i] is None:
                    respuesta[i] = var > 0
                    asignados += 1
            if asignados == self.num_vars:
                break
        return respuesta

def algoritmo():
    num_vars, num_clausulas = map(int, input().split())
    clausulas = [list(map(int, input().split())) for _ in range(num_clausulas)]

    sat = DosSAT(num_vars, clausulas)
    resultado = sat.es_satisfactible()
    if resultado is None:
        print("UNSATISFIABLE")
    else:
        print("SATISFIABLE")
        print(" ".join(str(i + 1 if resultado[i] else -i - 1) for i in range(num_vars)))


if __name__ == "__main__":
    algoritmo()
