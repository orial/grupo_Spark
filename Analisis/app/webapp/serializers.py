from rest_framework import serializers
from webapp.models import Incident

class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = ('year', 'district', 'incidentid', 'subid', 'address')
