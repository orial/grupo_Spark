# Fase II: Análisis de datos con Python

* [Introducción](#introducción)
* [Conectores](#conectores)
  * [Cassandra](#cassandra)
  * [Mongodb](#mongodb)
  * [Neo4j](#neo4j)
* [Vistas](#vistas)
  * [Cassandra](#vistas-cassandra)
  * [Mongodb](#vistas-mongo)
  * [Neo4j](#vistas-neo4j)

----

## Introducción


## Conectores


## Vistas

Hemos generalizado los tipos de consultas dependendiendo a las expectativas sobre la aplicación, 
todas ellas se encuentran reflejadas como tablas en las correspondientes vistas:

* Obtener toda las incidencias para un periodo de tiempo (rango). 
* Actividad criminal por zona
* Actividad criminal por tipo de delito
* Nº incidencias agrupadas por zona / *año*
* Nº incidencias agrupadas por delito / *año*

Todas se pueden encontrar implementadas bajo:

* [Neo4j](neo4j/readme.md#vistas)
* [Mongodb](mongodb/readme.md#vistas)
* [Cassandra](cassandra/readme.md#vistas)

### Vistas Cassandra







## Referencias

* Cassandra: https://github.com/pycassa/pycassa

* Paginator: https://simpleisbetterthancomplex.com/tutorial/2016/08/03/how-to-paginate-with-django.html

* Maps: http://blog.mathieu-leplatre.info/geodjango-maps-with-leaflet.html
