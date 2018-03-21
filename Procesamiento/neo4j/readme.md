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

### Actualización

Mientras que en el archivo sólo se guarda la fecha como cadena de caracteres en la columna *Date*, en el esquema aparecen tres campos: *Day*,*Month* y *Year*, los cuales serán obtenidos durante el siguiente apartado.

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

Que se utilizaría para la carga de datos en el siguiente apartado.

### Actualización

Sin embargo, encontramos un problemas con el formato actual. Este consiste en que el campo *Date* no nos proporciona acceso individual a cada variable (Día, mes y año). Obtener estas dividiendo la columna en una sentencia **cipher** aumenta de forma exponencial el tiempo de carga del CSV a la base de datos, por lo tanto es recomendable realizar esta operación anteriormente y modificar el archivo existente:

```
# Transformamos las columas del data.frame para poder operar sobre ellas.
SF_Crime_Ordered_Map_2 <- data.frame(lapply(SF_Crime_Ordered_Map, as.character), stringsAsFactors=FALSE)
# Usamos la librería stringr para mayor facilidad a la hora de separar la columna
install.packages("stringr")
library("stringr")

# Almacenamos los tres vectores resultantes
fechaSeparada <- str_split_fixed(SF_Crime_Ordered_Map_2$Date,'/',3)

# Añadimos al data.frame original las nuevas columnas y lo exportamos
SF_Crime_Ordered_Map$Day = fechaSeparada[,2]
SF_Crime_Ordered_Map$Month <- fechaSeparada[,1]
SF_Crime_Ordered_Map$Year <- fechaSeparada[,3]

write.csv(SF_Crime_Ordered_Map, "SF_Crime_Ordered_Date_Map.csv", row.names = FALSE)
```

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
  CREATE INDEX ON :DATE(day);
  CREATE INDEX ON :DATE(month);
  CREATE INDEX ON :DATE(year);
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

### Actualización

Para cargar los nuevos datos de día, mes y año, la query tuvo que cambiar a:

```
USING PERIODIC COMMIT 5000
LOAD CSV WITH HEADERS FROM 'file:///SF_Crime_Ordered_Date_Map.csv' AS line 
CREATE (i:INCIDENT {  incidentNum:toInteger(line.IncidntNum), description:line.Descript})
MERGE (c:CATEGORY {  name: line.Category})
MERGE (f:DATE {  day:toInteger(line.Day), month:toInteger(line.Month),year:toInteger(line.Year)})
ON CREATE SET f.dayofweek = line.DayOfWeek
MERGE (r:RESOLUTION { name: line.Resolution})
MERGE (d:DISTRICT { name:line.PdDistrict})
CREATE (i)-[t:TYPE]->(c),
(i)-[p:PLACE { address:line.Address,  x:line.X,  y:line.Y}]->(d),
(i)-[ti:TIME {time: line.Time}]->(f),
(i)-[s:STATUS]->(r);
```

La cual es ciertamente más lenta, debido a que se han añadido tipados en **:INCIDENT** y **:DATE**, además de que el **MERGE** realizado en este segundo tipo de nodo debe comparar dos variables adicionales para no causar duplicidad, aumentando la duración de la carga a **14m**.

#### *¿Por qué este cambio?*

La subida de datos a servidor es algo que sólo se debe realizar una vez, por tanto es absolutamente más eficiente que tarde más este paso, que ralentizar las búsquedas teniendo que filtrar la fecha con comparadores de cadenas de caracteres en cada una.

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

* Número de incidencias por año/día (por tipo de delito)

```
MATCH (n:INCIDENT)-->(s:DATE) return s,count(n); // Incidentes por día
MATCH (n:INCIDENT)-->(s:DATE) return s.year,count(n) // Incidentes por año
MATCH (c:CATEGORY)<--(n:INCIDENT)-->(s:DATE) return s.year,c.name,count(n) order by c.name // Incidentes y su tipo, por año
MATCH (c:CATEGORY)<--(n:INCIDENT)-->(s:DATE) return s,c.name,count(n) order by c.name // Incidentes y su tipo, por día
```
* Frecuencia de incidencias por día de la semana

```
MATCH (n:INCIDENT)-->(s:DATE) return s.dayofweek,s.year,count(n) order by s.dayofweek,s.year // Totales de incidentes los días de la semana de cada año
```

