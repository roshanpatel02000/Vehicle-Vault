from django import forms  # type: ignore
from .models import Accessory, VehicleAccessoryMap  # type: ignore

class AccessoryForm(forms.ModelForm):
    class Meta:
        model = Accessory
        fields = ['accessory_name', 'vehicle_type', 'brand', 'price', 'image', 'description', 'availability']
        widgets = {
            'accessory_name': forms.TextInput(attrs={'class': 'dark-input', 'placeholder': 'Accessory Name'}),
            'vehicle_type': forms.TextInput(attrs={'class': 'dark-input', 'placeholder': 'Compatible Vehicle Type (SUV, Sedan...)'}),
            'brand': forms.TextInput(attrs={'class': 'dark-input', 'placeholder': 'Brand'}),
            'price': forms.NumberInput(attrs={'class': 'dark-input', 'placeholder': 'Price'}),
            'description': forms.Textarea(attrs={'class': 'dark-input', 'placeholder': 'Accessory details...', 'rows': 4}),
            'availability': forms.CheckboxInput(attrs={'class': 'dark-checkbox'}),
        }

class VehicleAccessoryMapForm(forms.ModelForm):
    class Meta:
        model = VehicleAccessoryMap
        fields = ['vehicle', 'accessory']
        widgets = {
            'vehicle': forms.Select(attrs={'class': 'dark-input'}),
            'accessory': forms.Select(attrs={'class': 'dark-input'}),
        }
