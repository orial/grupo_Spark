# Analisis de datos con Python y Cassandra

## Introducción

*cassandra.cluster*. Contiene una clase principal denominada *Cluster* que se conecta a un cluster de Cassandra estableciendo
una conexión encapsulada en el objeto _Session_. Se pueden añadir ciertas configuraciones en acorde a la arquictura definida o a la forma 
de conexión: 

Ventajas:

  * Permite balanceo de carga entre los nodos disponibles
  * Pool de threads para conexiones
  * Permite añadir una capa de seguridad

Toda esta información esta reflejada en el documento oficial que podemos encontrar bajo [https://datastax.github.io/python-driver/api/cassandra/cluster.html]].

A este nivel encontramos tres documentos que representan a las funciones que permitan obtener las vistas en python
y se encuentran alojados bajo un informe (notebook) creado con la herramienta Jupyter.

* [Notebook](Analisis-Cassandra.ipynb)
* [Salida formato html](Analisis-Cassandra.html) / [pdf](Analisis-Cassandra.pdf)

## Configuración e instalación del conector / compatibilidad con Django

```
pip install cassandra-driver
pip install django-cassandra-engine
```

### Macos

```
 brew install libev
```

## Peculiaridades

## Como realizar migraciones de datos

https://medium.com/@cobli/the-best-way-to-manage-schema-migrations-in-cassandra-92a34c834824

Summarizing, the cassandra-migrate tool has the following features:

* Written in Python for easy installation
* Does not require cqlsh, just the Python driver
* Supports baselining an existing database into versions
* Supports unique environments for multiple profiles
* Supports partial advancement
* Supports locking for concurrent instances using Lightweight Transactions
* Verifies stored migrations against configured migrations
* Stores content, checksum, date and state of every migration
+ Supports deploying with different keyspace configurations for different environments


https://www.slothparadise.com/how-to-install-and-use-cassandra-on-django/

```
