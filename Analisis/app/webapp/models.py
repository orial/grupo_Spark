


# example/models.py
#https://datastax.github.io/python-driver/api/cassandra/cqlengine/models.html
#http://cqlengine.readthedocs.io/en/latest/topics/models.html
import uuid
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from django.db import models
from django_cassandra_engine.models import DjangoCassandraModel

class Incident(DjangoCassandraModel):
    __table_name__ = 'overall'
    year = columns.Integer(primary_key=True, partition_key=True)
    district = columns.Text()
    incidentid = columns.Integer()
    subid = columns.Integer()
    address = columns.Text()

"""CREATE TABLE if not exists incidents.overall (
    year int,
    district text, example_id    = columns.UUID(primary_key=True, default=uuid.uuid4)
     example_type  = columns.Integer(index=True)
     created_at    = columns.DateTime()
     description   = columns.Text(required=False)
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
    PRIMARY KEY ((year), time, incidentId, subid)
) WITH CLUSTERING ORDER BY (time DESC, incidentId DESC, subid DESC);"""

"""class ExampleModel(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    read_repair_chance = 0.05 # optional - defaults to 0.1
    example_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    description = columns.Text(required=False)"""

