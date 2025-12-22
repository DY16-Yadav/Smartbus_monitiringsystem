from django.contrib import admin
from .models import BusData

@admin.register(BusData)
class BusDataAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'bus_number',
        'latitude',
        'longitude',
        'speed',
        'temperature',
        'fuel_percent',
        'fuel_level',
        'timestamp',
    )
    list_filter = ('bus_number', 'timestamp')
    search_fields = ('bus_number',)
