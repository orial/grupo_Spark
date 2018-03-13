# Mongodb

# Requirements
* Mongodb

## Installation
* Download mongodb
* Download Compass
* Run mongo (recordar poner en el path)

## Importing csv
* Descargamos csv desde la web:
  * Forma 1: en consola escribimos  "mongoimport -d datascience -c incidents --type csv --file Incidents.csv --headerline"
  * Forma 2: Hemos escrito un scripy en python2, load_data.py que realiza la misma funcion

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

