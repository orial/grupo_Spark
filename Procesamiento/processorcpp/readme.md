# CPPProcessor

The application ```processor``` will export stats information into few files with the calculated information based on imported source TSV file
passed as argument:

* Incidents count by categories: _indicentsByCategory.tsv_
* Incidents count by districts:  _indicentsByDistrict.tsv_

## Getting started

```
$ g++ -g -o processor app.cpp
$ ./processor sample.tsv
```

## How to use

```
$ ./processor sample.tsv
First Incident:GRAND THEFT FROM LOCKED AUTO
First occurence of Filtered Incident by dayoftheweek:GRAND THEFT FROM LOCKED AUTO,Monday

Exporting incidents count by district into filename: incidentsByDistrict.tsv ...
Incidents groups:6

Exporting incidents count by category into filename: incidentsByCategory.tsv ...
Incidents groups:1
```

It returns two files with the information processed:

_incidentsByDistrict.tsv_
```
bayview	    1
central	    1
ingleside	1
mission	    2
northern	2
southern	3
```

_incidentsByCategory.tsv_
```
larceny/theft	10
```

## References
* C++ Concurrency in action (Chapter 8) [book](http://www.bogotobogo.com/cplusplus/files/CplusplusConcurrencyInAction_PracticalMultithreading.pdf)

* Split lines into record variables 
https://stackoverflow.com/questions/15701015/split-and-process-a-string-in-c-into-different-variables


## Contributors
* Álvaro vrandkode@gmail.com