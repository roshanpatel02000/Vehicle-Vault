from django.db import models
from django.conf import settings


class Vehicle(models.Model):
    FUEL_CHOICES = [
        ('Petrol', 'Petrol'),
        ('Diesel', 'Diesel'),
        ('Electric', 'Electric'),
        ('Hybrid', 'Hybrid'),
        ('CNG', 'CNG'),
    ]
    TRANSMISSION_CHOICES = [
        ('Manual', 'Manual'),
        ('Automatic', 'Automatic'),
    ]
    BODY_CHOICES = [
        ('SUV', 'SUV'),
        ('Sedan', 'Sedan'),
        ('Hatchback', 'Hatchback'),
        ('Coupe', 'Coupe'),
        ('Convertible', 'Convertible'),
        ('Pickup', 'Pickup'),
        ('MUV', 'MUV'),
        ('Crossover', 'Crossover'),
    ]

    brand               = models.CharField(max_length=100)
    model               = models.CharField(max_length=100)
    variant             = models.CharField(max_length=100, blank=True, null=True)
    price               = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.IntegerField(blank=True, null=True)
    offer_price         = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fuel_type           = models.CharField(max_length=50, choices=FUEL_CHOICES)
    transmission        = models.CharField(max_length=50, choices=TRANSMISSION_CHOICES)
    engine              = models.CharField(max_length=100)
    mileage             = models.DecimalField(max_digits=5, decimal_places=2)
    seating_capacity    = models.IntegerField()
    body_type           = models.CharField(max_length=50, choices=BODY_CHOICES, blank=True, null=True)
    color               = models.CharField(max_length=50, blank=True, null=True)
    description         = models.TextField(blank=True, null=True)
    image_file          = models.ImageField(upload_to='vehicles/', blank=True, null=True)
    image_url           = models.URLField(max_length=255, blank=True, null=True)
    is_featured         = models.BooleanField(default=False)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Vehicle'
        verbose_name_plural = 'Vehicles'

    def __str__(self):
        return f"{self.brand} {self.model} ({self.variant or 'Base'})"

    def get_display_price(self):
        return self.offer_price if self.offer_price else self.price

    def get_display_image(self):
        if self.image_file:
            return self.image_file.url
        return self.image_url or ''

    def to_dict(self):
        """Return a serializable dict of comparison-relevant fields."""
        return {
            'id': self.pk,
            'name': f"{self.brand} {self.model}" + (f" {self.variant}" if self.variant else ""),
            'brand': self.brand,
            'model': self.model,
            'variant': self.variant or '',
            'price': str(self.price),
            'offer_price': str(self.offer_price) if self.offer_price else None,
            'discount_percentage': self.discount_percentage,
            'fuel_type': self.fuel_type,
            'transmission': self.transmission,
            'engine': self.engine,
            'mileage': str(self.mileage),
            'seating_capacity': self.seating_capacity,
            'body_type': self.body_type or '',
            'color': self.color or '',
            'image': self.get_display_image(),
        }


class VehicleComparison(models.Model):
    vehicle1         = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='compared_as_first')
    vehicle2         = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='compared_as_second')
    compared_by      = models.ForeignKey(
                           settings.AUTH_USER_MODEL,
                           on_delete=models.SET_NULL,
                           null=True, blank=True,
                           related_name='comparisons',
                       )
    comparison_date  = models.DateTimeField(auto_now_add=True)
    similarity_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    best_vehicle     = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        ordering = ['-comparison_date']
        verbose_name = 'Vehicle Comparison'
        verbose_name_plural = 'Vehicle Comparisons'

    def __str__(self):
        return f"{self.vehicle1} vs {self.vehicle2} ({self.comparison_date.strftime('%d %b %Y')})"
