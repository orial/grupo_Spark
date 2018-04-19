import neo4j.v1
from neo4j.v1 import GraphDatabase

class Neo4JCrime(object):

    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def changepassword(self,newpass):
        with self._driver.session() as session:
            session.run(f'CALL dbms.changePassword("{newpass}")')

    """
        ===========================================================
                        Métodos de selección
        Los métodos de selección devuelven un listado de filas en 
        forma de diccionarios. Pueden tomar un nombre de label o 
        no.
        ===========================================================
    """
    @staticmethod
    def select_nodes_limited(tx, name,limit):

        name = ':'+name if name is not None else ''

        query = f"MATCH (N{name.upper()}) RETURN N,id(N) as id LIMIT $limit"
        result = tx.run(query,limit=limit)
        return result

    @staticmethod
    def select_nodes(tx, name):

        name = ':' + name if name is not None else ''

        query = f"MATCH (N{name.upper()}) RETURN N,id(N) as id"
        result = tx.run(query)
        return result

    @staticmethod
    def select_nodes_count(tx, name):

        name = ':' + name if name is not None else ''

        query = f"MATCH (N{name.upper()}) RETURN COUNT(N) as count"
        result = tx.run(query)
        return result

    @staticmethod
    def select_nodes_custom(tx,query):
        result = tx.run(query)
        return result

    # Tratar resultados
    """
        @:argument (result): 'neo4j.v1.result.BoltStatementResult'.
        @:returns (listRes): 'list of dictionaries' / 'single dictionary'

        Esta función coge un objeto salida de una transacción Neo4J, en general, una lectura.
        Por cada fila obtenida, crea un diccionario con labels, propiedades de los nodos obtenidos.
        Mete estos diccionarios en una lista. Si solo hay un elemento, devuelve un diccionario.

        ATENCION, los nodos tienen APODOS, para acceder a sus propiedades hay que hacerlo mediante
        listRes[numRow]["APODO.PROPIEDAD"]
    """
    @staticmethod
    def result_as_list(result):
        listRes = [];

        for i, l in enumerate(result.records()):
            listRes.insert(i, dict())
            for k, v in l.items():
                # print(k,'->',v) # Aquí está el nodo y el nombre de la clave, además de otros resultados
                if isinstance(v, neo4j.v1.types.Node):
                    listRes[i][f"{k}.labels"] = v.labels
                    listRes[i] = {**listRes[i], **{k + '.' + key: val for key, val in iter(v.properties.items())}}
                elif isinstance(v,neo4j.v1.types.Relationship):
                    listRes[i] = {f'{k}.type':v.type}
                    listRes[i] = {**listRes[i], **{f'{k}.{key}': val for key, val in iter(v.properties.items())}}
                else:
                    listRes[i][k] = v
        return listRes

    # SELECCIONAR
    """
        Método de selección con nombre de un label como máximo. No tiene límite.
    """
    def select(self, name = None):

        result = None

        with self._driver.session() as session:
            result  = session.read_transaction(self.select_nodes, name)

        return self.result_as_list(result)

    # SELECCIONAR LIMITADO
    """
        Método de selección con nombre de un label como máximo y es posible limitar el número de filas.
        Mínimo 1 filas. 
    """
    def select_limit(self,name=None,limit=1):

        result = None

        with self._driver.session() as session:
            result = session.read_transaction(self.select_nodes_limited,name,limit)

        return self.result_as_list(result)

    # SELECCIONAR CONTAR
    """ 
        Método de selección de número de nodos, acepta un label como máximo.
    """
    def select_count(self,name=None):

        result = None

        with self._driver.session() as session:
            result = session.read_transaction(self.select_nodes_count,name)

        return result.single()[0]

    # SELECCIONAR CUSTOMIZADO
    """
        Método de selección sobre query directa, se escribe la query en Cypher y se devuelve el resultado.
    """
    def select_custom(self,query):

        result = None

        with self._driver.session() as session:
            result = session.read_transaction(self.select_nodes_custom,query)

        return self.result_as_list(result)

    # SELECCIONAR PROPIEDADES
    """
        Método que devuelve todas las posibles propiedades para un nodo.
        El argumento es obligatorio.
    """
    def select_node_properties(self,name):

        result = None
        name = f':{name}' if name is not None else ''

        query = f"MATCH (N{name}) RETURN DISTINCT keys(N) as properties, labels(N) as label"

        with self._driver.session() as session:
            result = session.read_transaction(self.select_nodes_custom,query)

        return self.result_as_list(result)

    # SELECCIONAR LABELS
    """
        Método que devuelve todos los labels disponibles para los nodos.
    """
    def select_node_labels(self):

        result = None

        query = f"MATCH (N) RETURN DISTINCT labels(N) as label"

        with self._driver.session() as session:
            result = session.read_transaction(self.select_nodes_custom,query)

        return self.result_as_list(result)

    # SELECCIONAR TIPOS DE RELACIONES
    """
        Método para ver los tipos de relaciones entre dos nodos, si no se dan argumentos, devuelve todos los tipos.
    """
    def select_relationship_kind(self,name=None,name2=None):

        result = None
        name = f':{name}' if name is not None else ''
        name2 = f':{name2}' if name2 is not None else ''

        query = f"MATCH (N{name})-[r]->(E{name2}) RETURN DISTINCT type(r) as tipo"

        with self._driver.session() as session:
            result = session.read_transaction(self.select_nodes_custom,query)

        return self.result_as_list(result)

# INSERTAR UNO

# INSERTAR VARIOS

# BORRAR

# BORRAR UNO

# ACTUALIZAR




try:
    h = Neo4JCrime('bolt://localhost:7687','test','4321')

    var = h.select_count()

    print(var)

    var = h.select_limit('CATEGORY',6)

    print(var)

    var = h.select_custom('MATCH (N:CATEGORY) RETURN N LIMIT 10')

    for i in range(0,len(var)):
        for k,v in var[i].items():
            print(k,'->',v)


    var = h.select_custom('MATCH (N:INCIDENT)-[R]->(C) RETURN N,R,C LIMIT 10')

    for i in range(0,len(var)):
        print(var[i])
        """
        for k,v in var[i].items():
            print(k,'->',v)
        """
    var = h.select_relationship_kind()

    print(var)

    var = h.select_node_labels()

    print(var)

    temp = var;

    for x in iter(temp):
        for k,v in x.items():
            var = h.select_node_properties(v[0])

            print(var)



except Exception as e:
    print(e)

#input('Press ENTER to exit')
