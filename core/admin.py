from django.contrib import admin
from .models import Team, Employee, Aircraft, Part

"""
Admin yönetimi için oluşturulan sınıf.
"""

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'team_type')

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'team')

@admin.register(Aircraft)
class AircraftAdmin(admin.ModelAdmin):
    list_display = ('aircraft_type', 'production_time')

@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ('id', 'part_type', 'team', 'aircraft', 'used', 'get_target_aircraft_type')

    def get_target_aircraft_type(self, obj):
        return obj.target_aircraft_type
    get_target_aircraft_type.short_description = 'Hedef Uçak Tipi'
