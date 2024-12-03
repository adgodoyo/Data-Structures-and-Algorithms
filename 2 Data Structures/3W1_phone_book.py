class Query:
    def __init__(self, query):
        self.type = query[0]
        self.number = int(query[1])
        if self.type == 'add':
            self.name = query[2]

def read_queries():
    n = int(input())
    return [Query(input().split()) for _ in range(n)]

def write_responses(result):
    print('\n'.join(result))

def process_queries(queries):
    result = []
    contacts = {}

    for cur_query in queries:
        if cur_query.type == 'add':
            # Sobrescribir o agregar un contacto
            contacts[cur_query.number] = cur_query.name
        elif cur_query.type == 'del':
            # Eliminar un contacto si existe
            if cur_query.number in contacts:
                del contacts[cur_query.number]
        elif cur_query.type == 'find':
            # Buscar un contacto
            response = contacts.get(cur_query.number, 'not found')
            result.append(response)

    return result

if __name__ == '__main__':
    write_responses(process_queries(read_queries()))
