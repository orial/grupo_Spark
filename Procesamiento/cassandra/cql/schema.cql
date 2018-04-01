/* Creating keyspace */
create keyspace if not exists incidents 
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1' };

/*                              */
/* Creating overall incidents   */
/*

/* Creating scheme  */
CREATE TABLE if not exists incidents.overall (
    incidentId bigint,
    subid bigint,
    address text,
    category text,
    dayoftheweek text,
    description text,
    district text,
    location text,
    resolution text,
    time timestamp,
    year int,
    month int,
    day int,
    hour int,
    x text,
    y text,
    PRIMARY KEY ((incidentId,subid), time)
) WITH CLUSTERING ORDER BY (time DESC);

CREATE INDEX overall_index_incidentid ON incidents.overall (incidentId);
CREATE INDEX overall_index_subid ON incidents.overall (subid);

/* Importing dataset */
COPY incidents.overall(incidentId, category, description, dayoftheweek, time, day,year,month, hour, district, resolution, address,x,y,location, subid) 
FROM '/Users/vrandkode/Workspace/M2/CienciaDatosII_112/repository/grupo_Spark/Procesamiento/dataset/incidents.dataset.sample.100.csv' 
WITH DELIMITER=';' and HEADER=false and DATETIMEFORMAT='%Y-%m-%d %H:%M:%S';


/*                                      */
/* Creating incidents by district/year  */
/*

/* Creating scheme  */
CREATE TABLE if not exists incidents.bydistrict (
    year int,
    district text,
    incidentId bigint,
    subid bigint,
    address text,
    category text,
    dayoftheweek text,
    description text,
    location text,
    resolution text,
    time timestamp,
    month int,
    day int,
    hour int,
    x text,
    y text,
    PRIMARY KEY ((year,district), time, month, day, hour)
) WITH CLUSTERING ORDER BY (time DESC, month DESC, day DESC,hour DESC);
CREATE INDEX bydistrict_index_year ON incidents.bydistrict (year);

/* Importing dataset from original table */
COPY incidents.overall (year, district, incidentId, subid, address, category, dayoftheweek, description, location, resolution, time, month, day, hour,x,y) 
TO 'tmp_incidents_by_district.csv';
COPY incidents.bydistrict(year, district, incidentId, subid, address, category, dayoftheweek, description, location, resolution, time, month, day, hour,x,y) 
FROM 'tmp_incidents_by_district.csv';


/*                                      */
/* Creating incidents by category/year  */
/*

/* Creating scheme  */
CREATE TABLE if not exists incidents.bycategory (
    year int,
    category text,
    incidentId bigint,
    subid bigint,
    address text,
    district text,
    dayoftheweek text,
    description text,
    location text,
    resolution text,
    time timestamp,
    month int,
    day int,
    hour int,
    x text,
    y text,
    PRIMARY KEY ((year,category), time, month, day, hour)
) WITH CLUSTERING ORDER BY (time DESC, month DESC, day DESC,hour DESC);
CREATE INDEX bycategory_index_year ON incidents.bycategory (year);

/* Importing dataset from original table */
COPY incidents.overall (year, category, incidentId, subid, address, district, dayoftheweek, description, location, resolution, time, month, day, hour,x,y) 
TO 'tmp_incidents_by_category.csv';
COPY incidents.bycategory(year, category, incidentId, subid, address, district, dayoftheweek, description, location, resolution, time, month, day, hour,x,y) 
FROM 'tmp_incidents_by_category.csv';
