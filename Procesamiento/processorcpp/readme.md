# CPPProcessor


# ProcessorCPP

* [Introduction](#Introduction)

* [Primeros pasos](#primeros-pasos)
  * Requerimientos técnicos

* [Preprocesamiento e importación de datos](#preprocesamiento-e-importación-de-datos)

* [Estructura y Modelado de datos](#estructura-de-datos)

* [Consultas](#consultas)

* [Referencias](#referencias)

---

## Introducción

La aplicación ```processor``` exporta la información contenida en varios ficheros con la información detallada basada en el fichero inicial TSV recien preprocesado. EL fichero de entrada es especificado como argumento:

* Incidents count by categories: _indicentsByCategory.tsv_
* Incidents count by districts:  _indicentsByDistrict.tsv_

## Primeros pasos

```
$ g++ -g -o processor app.cpp
$ ./processor sample.tsv
```

### Requerimientos técnicos

* g++
* Visual studio Code (IDE)

## Preprocesamiento e importación de datos

La aplicación preprocesa los datos y realiza la importación de forma automática, mediante la clase ```Incidents::import(filename)```.

```
$ ./processor sample.tsv
First Incident:GRAND THEFT FROM LOCKED AUTO
First occurence of Filtered Incident by dayoftheweek:GRAND THEFT FROM LOCKED AUTO,Monday

Exporting incidents count by district into filename: incidentsByDistrict.tsv ...
Incidents groups:6

Exporting incidents count by category into filename: incidentsByCategory.tsv ...
Incidents groups:1
```
## Estructura de datos

La información se encuentra desglosada en estructuras basada en listas de estructura tipo truct ``ìncident````

```
struct incident
{
  std::string id;
  std::string category;
  std::string description;
  std::string dayoftheweek;
  std::string time;
  std::string place;
  std::string resolution;
  std::string address;
  std::string x;
  std::string y;
  std::string location;
};
```
Mediante el método ```Íncidents::import(inputname)```el fichero CSV es procesado y transformado en un vector de estructuras tipo incident.

Con ayuda de los métodos de la clase *Incidents*: getByDistrict y getByCategory, en base al privado genérico getByAttribute; se pueden construir consultas de filtrado y de agregación de forma rápida:

```
/* Filtrar y agrupar por distrito */
std::map<std::string, vector<incident> > getByDistrict();
```
```
/* Filtrar y agrupar por categoria */
std::map<std::string, vector<incident> > getByCategory();
```

```    
std::map<std::string, vector<incident> > getByAttribute(const char * attribute);
```

Otros métodos de agrupación de índole genéricas son usados para realizar consultas de tipo *agregado*:

* Por zona ```void exportDistrictsCount(Incidents incidents, const char* filename)```
* Por distrito ```void exportCategoryCount(Incidents incidents, const char* filename)```


## Consultas

En la salida se recuperan dos ficheros con la información de las *consultas* realizadas:

 * Actividad criminal por distrito
 * Actividad criminal por categoria

### Actividad criminal por distrito

_incidentsByDistrict.tsv_
```
bayview	    1
central	    1
ingleside	1
mission	    2
northern	2
southern	3
```

### Actividad criminal por categoria

_incidentsByCategory.tsv_
```
larceny/theft	10
```


## Referencias
* C++ Concurrency in action (Chapter 8) [book](http://www.bogotobogo.com/cplusplus/files/CplusplusConcurrencyInAction_PracticalMultithreading.pdf)

* Split lines into record variables 
https://stackoverflow.com/questions/15701015/split-and-process-a-string-in-c-into-different-variables


## Contributors
* Álvaro vrandkode@gmail.com