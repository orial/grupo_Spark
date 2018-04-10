from django.shortcuts import render

from django.shortcuts import render
from django.http import HttpResponse

from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from cassandra.cluster import Cluster
from models import ExampleModel
from django.http import HttpResponse


def index(request):
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()
    session.set_keyspace('db')
    insert = ExampleModel(description="Hello world description")
    insert.save()
    cluster.shutdown()
    return HttpResponse("Hello world")

