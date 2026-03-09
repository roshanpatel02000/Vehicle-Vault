from django import forms
from .models import Vehicle

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = [
            'brand', 'model', 'variant', 'price', 'discount_percentage', 'offer_price',
            'fuel_type', 'transmission', 'engine', 'mileage', 'seating_capacity',
            'body_type', 'color', 'description', 'image_file', 'image_url', 'is_featured',
            'safety_rating'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
