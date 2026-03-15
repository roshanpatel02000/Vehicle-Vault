from django.contrib import admin  # type: ignore
from .models import Accessory, VehicleAccessoryMap  # type: ignore

@admin.register(Accessory)
class AccessoryAdmin(admin.ModelAdmin):
    list_display = ('accessory_name', 'vehicle_type', 'brand', 'price', 'availability')
    list_filter = ('vehicle_type', 'brand', 'availability')
    search_fields = ('accessory_name', 'brand', 'description')

@admin.register(VehicleAccessoryMap)
class VehicleAccessoryMapAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'accessory', 'created_at')
    list_filter = ('vehicle__brand', 'accessory__accessory_name')
    search_fields = ('vehicle__brand', 'vehicle__model', 'accessory__accessory_name')
