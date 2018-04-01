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



