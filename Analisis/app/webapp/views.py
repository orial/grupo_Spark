from django.shortcuts import render

from django.shortcuts import render
from django.http import HttpResponse

from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from cassandra.cluster import Cluster
from django.http import HttpResponse

from webapp.models import Incident
from webapp.serializers import IncidentSerializer

from rest_framework import generics

class IncidentList(generics.ListCreateAPIView):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer

class IncidentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer

def index(request):
    return render(request, 'index.html')

def overall(request):
    return render(request, 'incidents/overall.html', {'incidents': Incident.objects.all()})

