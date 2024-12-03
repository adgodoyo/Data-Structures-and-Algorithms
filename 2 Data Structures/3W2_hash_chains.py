class Query:

    def __init__(self, query):
        self.type = query[0]
        if self.type == 'check':
            self.ind = int(query[1])
        else:
            self.s = query[1]


class QueryProcessor:
    _multiplier = 263
    _prime = 1000000007

    def __init__(self, bucket_count):
        self.bucket_count = bucket_count
        # Inicializar listas separadas para cada bucket
        self.buckets = [[] for _ in range(bucket_count)]

    def _hash_func(self, s):
        ans = 0
        for c in reversed(s):
            ans = (ans * self._multiplier + ord(c)) % self._prime
        return ans % self.bucket_count

    def write_search_result(self, was_found):
        print('yes' if was_found else 'no')

    def write_chain(self, chain):
        print(' '.join(chain))

    def read_query(self):
        return Query(input().split())

    def process_query(self, query):
        if query.type == "check":
            # Imprimir los elementos en el bucket correspondiente
            self.write_chain(self.buckets[query.ind])
        else:
            hash_value = self._hash_func(query.s)
            chain = self.buckets[hash_value]

            if query.type == 'find':
                # Verificar si el elemento está en el bucket
                self.write_search_result(query.s in chain)
            elif query.type == 'add':
                # Agregar el elemento al inicio si no está presente
                if query.s not in chain:
                    chain.insert(0, query.s)
            elif query.type == 'del':
                # Eliminar el elemento si está presente
                if query.s in chain:
                    chain.remove(query.s)

    def process_queries(self):
        n = int(input())
        for _ in range(n):
            self.process_query(self.read_query())


if __name__ == '__main__':
    bucket_count = int(input())
    proc = QueryProcessor(bucket_count)
    proc.process_queries()
