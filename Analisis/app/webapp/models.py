# example/models.py
#https://datastax.github.io/python-driver/api/cassandra/cqlengine/models.html
#http://cqlengine.readthedocs.io/en/latest/topics/models.html

import uuid
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from django.db import models
from django_cassandra_engine.models import DjangoCassandraModel


## 
# Cassandra models
#

class IncidentsOverAllCassandra(DjangoCassandraModel):
    __table_name__ = 'overall'
    year = columns.Integer(primary_key=True, partition_key=True)
    district = columns.Text()
    incidentid = columns.Integer()
    subid = columns.Integer()
    address = columns.Text()

