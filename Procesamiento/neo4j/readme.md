# Neo4j

# Requirements
* Cassandra
* hsqlc

## Installation
* Download cassandra
* Run ./cassandra

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
## Data structure

## Queries

Necesitamos diseñar para cada tipo de de base de datos para poder listar las siguientes consultas:

* Número de incidencias por zona/dia

```
select *
```

* Número de incidencias por año/dia (por tipo de delito)

```
select *
```
* Frecuencia de incidencias por dia de la semana

```
select *
```

