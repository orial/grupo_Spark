# Cassandra

# Requirements
* Cassandra
* hsqlc

## Installation
* Download cassandra
* Run ./cassandra

## Importing Incidents data

* Downloading the Incidents dataset from _TSV for Excel_ version from https://data.sfgov.org/Public-Safety/Map-of-Police-Department-Incidents/gxxq-x39z and clean data before importing: removing the headers, transform and merge the date/time into time field. The results will be saved under incidents.tsv

```
wget -O- "https://data.sfgov.org/api/views/gxxq-x39z/rows.tsv?accessType=DOWNLOAD" |tail -n +2|sed -E 's/([0-9]+)\/([0-9]+)\/([0-9]+) ([0-9\:]+) [A-M]+.([0-9\:]+)/\3-\1-\2 \5:00/g' > incidents.tsv
```

* Creating keyspace (use _DevCenter_ or cql shell ```./datastax-ddc-3.9.0/bin/cqlsh```)
```
CREATE KEYSPACE incidents
WITH replication = {'class': 'SimpleStrategy',
'replication_factor' : 1};
```

* Create incidents table
```
CREATE TABLE IF NOT EXISTS incidents (
  id text PRIMARY KEY,
  category text,
  description ascii,
  dayoftheweek text,
  time timestamp,
  district text,
  resolution text,
  address text,
  x text,
  y text,
  location text
);
```

* Check if keyspace was created
```
cqlsh> describe keyspaces;

delitos        system_auth  incidents           system_traces
system_schema  system       system_distributed  personas
```

* Import data to table incidents
```
cqlsh> COPY incidents(id, category, description, dayoftheweek, time, district, resolution, address,x,y,location) 
FROM 'dataset/incidents.tsv' 
WITH DELIMITER='\t' and CHUNKSIZE=500 and INGESTRATE=2000 and HEADER=false and DATETIMEFORMAT='%Y-%m-%d %H:%M:%S';
```

```
Processed: 25210 rows; Rate:    1094 rows/s; Avg. rate:    2024 rows/s
25210 rows imported from 1 files in 12.453 seconds (0 skipped).
```

---

### Data modeling

From dasbhoard: [[http://kdm.dataview.org/kdm.jsp]]

## Queries

Tablas requeridas para realizar las consultas:

```
CREATE TABLE incidencias.category (category text, cyclist_name text, flag int STATIC, PRIMARY KEY (country, cyclist_name));
```



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

---
## Troubleshooting
### Is Cassandra running

Linux
```
netstat -ap tcp | grep -i "listen"|grep 9042
```

Macos
```
sudo lsof -PiTCP -sTCP:LISTEN|grep 9042
java      41458 vrandkode  190u  IPv4 0x32271e72c028899      0t0  TCP localhost:9042 (LISTEN)
```

### Installing DevCenter

* DevCenter closes bceause of java virtual machine
Edit DevCenter.app/Contents/devcenter.ini and add the line
```
-vm
/Library/Java/JavaVirtualMachines/jdk1.8.0_51.jdk/Contents/Home/bin
```





