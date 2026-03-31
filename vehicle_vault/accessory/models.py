from django.db import models
from django.conf import settings
from vehicle.models import Vehicle

class Accessory(models.Model):
    accessory_name = models.CharField(max_length=150)
    vehicle_type = models.CharField(max_length=100)  # e.g., SUV, Sedan, Hatchback
    brand = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='accessories/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    availability = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.accessory_name

    class Meta:
        verbose_name_plural = "Accessories"

class VehicleAccessoryMap(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='accessory_mappings')
    accessory = models.ForeignKey(Accessory, on_delete=models.CASCADE, related_name='vehicle_mappings')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('vehicle', 'accessory')
        verbose_name = "Vehicle Accessory Mapping"
        verbose_name_plural = "Vehicle Accessory Mappings"

    def __str__(self):
        return f"{self.vehicle} - {self.accessory}"

class FavouriteAccessory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favourite_accessories'
    )
    accessory = models.ForeignKey(
        Accessory,
        on_delete=models.CASCADE,
        related_name='favourited_by_users'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'accessory')
        ordering = ['-created_at']
        verbose_name = 'Favourite Accessory'
        verbose_name_plural = 'Favourite Accessories'

    def __str__(self):
        return f"{self.user} favourited {self.accessory}"
