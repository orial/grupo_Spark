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

## References
* C++ Concurrency in action (Chapter 8) [book](http://www.bogotobogo.com/cplusplus/files/CplusplusConcurrencyInAction_PracticalMultithreading.pdf)

* Split lines into record variables 
https://stackoverflow.com/questions/15701015/split-and-process-a-string-in-c-into-different-variables


## Contributors
* Álvaro vrandkode@gmail.com