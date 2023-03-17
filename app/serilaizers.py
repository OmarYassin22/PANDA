from rest_framework import serializers
from .models import *
class PatinetSerializer(serializers.ModelSerializer):
    class Meta:
        model=patient
        fields='__all__'
        read_only_field=['id']
class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model=report_appiontment
        fields='__all__'
class SecreatarySerializer(serializers.ModelSerializer):
    class Meta:
        model=secretary
        fields='__all__'
class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model=doctor
        fields='__all__'
        