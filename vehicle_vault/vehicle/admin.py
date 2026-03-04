from django.contrib import admin
from .models import Vehicle, VehicleComparison


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display  = ['brand', 'model', 'variant', 'price', 'offer_price', 'fuel_type', 'transmission', 'is_featured', 'created_at']
    list_filter   = ['fuel_type', 'transmission', 'body_type', 'is_featured']
    search_fields = ['brand', 'model', 'variant']
    list_editable = ['is_featured']
    ordering      = ['-created_at']


@admin.register(VehicleComparison)
class VehicleComparisonAdmin(admin.ModelAdmin):
    list_display  = ['vehicle1', 'vehicle2', 'compared_by', 'similarity_score', 'best_vehicle', 'comparison_date']
    list_filter   = ['comparison_date']
    search_fields = ['vehicle1__brand', 'vehicle2__brand', 'best_vehicle']
    readonly_fields = ['comparison_date']
    ordering      = ['-comparison_date']
