# Analisis de datos con Python y neo4j

El conector _neo4j-driver_está basado en el driver oficial de Neo4J para Python. Esto ha implicado una transformación de las funciones por defecto para poder obtener resultados que sean útiles más tarde para nuestra aplicación.

## Tipos en neo4j.v1

En Neo4j existen dos tipos de entidades sobre las que se basa el sistema de almacenamiento de datos: nodos y relaciones. Lo que significa que dentro del propio driver se han creado clases específicas para estos elementos.

A este nivel encontramos tres documentos que representan a las funciones que permitan obtener las vistas en python
y se encuentran alojados bajo un informe (notebook) creado con la herramienta Jupyter.

* [Notebook](Analisis-Neo4j.ipynb)
* [Salida formato html](Analisis-Neo4j.html)

## Conexión con Django models

Para la conexión del driver con la aplicación de Django necesitamos la reprenstación herdada del modelo,
para ello con ayuda la definición del conector en [[neo4jConnector.py]] en la siguiente fase se llevará a cabo.
