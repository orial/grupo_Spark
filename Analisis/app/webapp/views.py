from django.shortcuts import render

from django.shortcuts import render
from django.http import HttpResponse

from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from cassandra.cluster import Cluster
from django.http import HttpResponse

from django.core.files.storage import default_storage

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.fields.files import FieldFile
from django.views.generic import FormView
from django.views.generic.base import TemplateView
from django.contrib import messages

from webapp.models import Incident
from webapp.serializers import IncidentSerializer

from rest_framework import generics

class IncidentList(generics.ListCreateAPIView):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer

class IncidentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer

def home(request):
    return 

def index(request):
    return render(request, 'index.html')

def overall(request):
    return render(request, 'incidents/overall.html', {'incidents': Incident.objects.all()})

class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        messages.info(self.request, 'hello http://example.com')
        return context
 

