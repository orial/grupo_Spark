from django.conf.urls import url,include

from . import views

from webapp import views, models
from rest_framework import routers, serializers, viewsets

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'incidents', views.IncidentList)

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^all/', views.overall, name='incidents'),
    url(r'^api/', include('rest_framework.urls'))
]