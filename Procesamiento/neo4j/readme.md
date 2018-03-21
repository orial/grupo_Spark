# Neo4j

# Requirements
* Neo4j Desktop/Server
* R and RStudio

## Installation
* Download Neo4j Desktop
* Download R
* Download RStudio
* Run Neo4jDesktop
* Run RSTudio

## Importing csv

Steps to import csv

Es necesario utilizar el query:
```
LOAD CSV WITH HEADERS FROM 'file:///SF_Crime_Heat_Map.csv' as line return line
```
Para importar los datos de CSV a la base de datos, sin embargo esto no genera nodos ni relaciones.

También es importante recordar que el fichero ha de estar en la carpeta:

```
Application\neo4jDatabases\database-(numero)\installation-3.3.3\import
```
Pero se puede cambiar modificando el archivo neo4j.conf en la línea:

```
dbms.directories.import=import
```

Siendo "import" el directorio por defecto.

También se puede acceder a esta configuración desde la aplicación Desktop mediante:

My project->(Nombre de BD)->Settings

Que provee de un editor propio.

## Data structure

Dada la estructura del archivo .CSV proporcionado, titulado con los siguientes **headers**:

IncidntNum, Category, Descript, DayOfWeek, Date, Time, PdDistrict, Resolution, Address, X, Y, Location.

Se ha decidido realizar este diseño de nodos y relaciones:

![alt text](https://image.ibb.co/ncrBcx/Nodos.jpg)

Dado que, a excepción de los incidentes, un gran número de elementos estaban duplicados, se ha procedido a crear sus propios nodos y a evitar su inserción múltiple. Los datos que podían causar la aparición doble de un mismo valor, como un distrito con mismo nombre pero coordenadas X e Y diferentes a las de otro mismo distrito, se han añadido a las relaciones entre los nodos de incidentes y el resto. Esto aumenta la eficiencia y rendimiento final tanto de la inserción como de las búsquedas futuras.

## Data formatting

Aunque en primer lugar no era necesario, tras causar cierto error en __Cypher__ relacionado con la ausencia de una propiedad en una operación __MERGE__, se procedió a buscar el motivo de este fallo en el archivo *SF_Crime_Heat_Map.csv* descargado directamente de la fuente.

![alt_text](https://image.ibb.co/bziqHx/error.jpg)

En **RStudio** se importó el dataset al completo, reemplazando los valores nulos con NA. Sin embargo, al iterar sobre el dataframe, el número de filas que [complete.cases]() devolvía era el mismo que el número de líneas del dataset original.


```
# R
SF_Crime_Heat_Map <- read.csv("C:/Users/Julio/Desktop/SF_Crime_Heat_Map.csv")
View(SF_Crime_Heat_Map)
missing <- SF_Crime_Heat_Map[complete.cases(SF_Crime_Heat_Map),]
nrow(SF_Crime_Heat_Map) == nrow(missing)
# [1] TRUE
```

Por tanto se decidió exportar estos mismos datos pero aprovechando el tipado que se había producido en la importación para ordenar el dataframe mediante el *incidentNum*. Este sería exportado a un nuevo archivo *SF_Crime_Ordered_Map.csv*.

```
# R
SF_data <- SF_Crime_Heat_Map[order(SF_Crime_Heat_Map$IncidntNum),]
View(SF_data)
write.csv(SF_data,"SF_Crime_Ordered_Map.csv")
```

Que se utilizará para la carga de datos en el siguiente apartado.

## Loading data into Neo4J

Esta fue la primera sentencia **Cypher** utilizada para cargar los datos.

* El tag **WITH HEADERS** de la instrucción **LOAD CSV** nos permite referirnos a las columnas por los nombres originales situados al comienzo del csv.
* Donde **MATCH** es similar a **SELECT** y **CREATE** a **INSERT**, respectivamente, **MERGE** es una mezcla entre ambos que busca el elemento especificado, y si no lo encuentra, lo crea, lo que conlleva una búsqueda previa a la potencial inserción.
* Los elementos como *nodos* y *relaciones* se especifican con **LABELS** y **Properties**, donde los primeros actuan como tipo principal del elemento y sirven para filtrarlos más fácilmente, y los segundos almacenan datos más específicos por lo que requieren sentencias con **WHERE** para su filtrado.

```
LOAD CSV WITH HEADERS FROM 'file:///SF_Crime_Ordered_Map.csv' AS line
CREATE (i:INCIDENT {  incidentNum:toInt(line.IncidntNum), description:line.Descript})
MERGE (c:CATEGORY {  name: line.Category})
MERGE (f:DATE {  date: line.Date,  diaSemana: line.DayOfWeek})
MERGE (r:RESOLUTION { name: line.Resolution})
MERGE (d:DISTRICT { name:line.PdDistrict})
CREATE (i)-[t:TYPE]->(c),
(i)-[p:PLACE { address:line.Address,  x:line.X,  y:line.Y}]->(d),
(i)-[ti:TIME {time: line.Time}]->(f),
(i)-[s:STATUS]->(r);
```
Problema de esta sentencia:
* Las sentencias MERGE buscan nodos con las mismas propiedades y labels antes de insertar lo que ralentiza la carga.
* La sentencia completa intenta realizarse con la memoria RAM actual, con 2M de datos por procesar.


Esto resultaba en errores de memoria o tiempos demasiado largos para la importación (una hora y media).

Qué se hizo:
* Se añadió la instrucción *USING PERIODIC COMMIT* la cual almacena los cambios realizados cada 1000 líneas, por defecto.
* Se añadió la instrucción *ON CREATE SET* que condiciona una propiedad de un nodo a su creación en *Merge*, mejorando la eficiencia.
* Se incluyeron índices antes de la carga para cada nodo, mejorando la velocidad de búsqueda:
  ```
  CREATE INDEX ON :INCIDENT(incidentNum);
  CREATE INDEX ON :CATEGORY(name);
  CREATE INDEX ON :DATE(date);
  CREATE INDEX ON :RESOLUTION(name);
  CREATE INDEX ON :DISTRICT(name);
  ```
  * Se aumentó la memoria modificando el archivo *neo4j.conf* con estos valores:
    ```
    dbms.memory.heap.initial_size=2G
    dbms.memory.heap.max_size=4G
    dbms.memory.pagecache.size=4G
    ````
    Lo cual aumentaba la memoría máxima utilizable por **Neo4j** hasta 8Gb de RAM.
    
Por tanto la sentencia final fue esta:

```
USING PERIODIC COMMIT 5000
LOAD CSV WITH HEADERS FROM 'file:///SF_Crime_Ordered_Map.csv' AS line
CREATE (i:INCIDENT {  incidentNum:line.IncidntNum, description:line.Descript})
MERGE (c:CATEGORY {  name: line.Category})
MERGE (f:DATE {  date: line.Date})
ON CREATE SET f.dayofweek = line.DayOfWeek
MERGE (r:RESOLUTION { name: line.Resolution})
MERGE (d:DISTRICT { name:line.PdDistrict})
CREATE (i)-[t:TYPE]->(c),
(i)-[p:PLACE { address:line.Address,  x:line.X,  y:line.Y}]->(d),
(i)-[ti:TIME {time: line.Time}]->(f),
(i)-[s:STATUS]->(r);
```

Que importaba los datos, creaba los nodos y sus relaciones en un tiempo de **3m20s**.

## Queries

Necesitamos diseñar para cada tipo de de base de datos para poder listar las siguientes consultas:

* Número de incidencias por día. **Count** es una función agregativa que reúne todas las entradas de un mismo tipo.

```
MATCH (n:INCIDENT)-[r:TIME]->(d:DATE) return d,count(n)
```

* Número de incidencias por zona.

```
MATCH (n:INCIDENT)-[r:PLACE]->(d:DISTRICT) return distinct d,count(n)
```

* Número de incidencias por año/dia (por tipo de delito)

```
select *
```
* Frecuencia de incidencias por dia de la semana

```
select *
```

