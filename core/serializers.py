from rest_framework import serializers
from .models import Team, Employee, Aircraft, Part

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'team_type']

class EmployeeSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)
    
    class Meta:
        model = Employee
        fields = ['id', 'user', 'team']

class AircraftSerializer(serializers.ModelSerializer):
    produced_by = serializers.CharField(source='produced_by.name', read_only=True)

    class Meta:
        model = Aircraft
        fields = ['id', 'aircraft_type', 'production_time', 'produced_by']

class PartSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(source='team.name', read_only=True)

    class Meta:
        model = Part
        fields = ['id', 'part_type', 'team', 'team_name', 'aircraft', 'production_time', 'used', 'target_aircraft_type']
