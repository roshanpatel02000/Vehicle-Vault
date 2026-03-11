from django.core.management.base import BaseCommand
from vehicle.models import Vehicle
from decimal import Decimal
import random

class Command(BaseCommand):
    help = 'Populates the database with 5 vehicles for each body type (40 total)'

    def handle(self, *args, **options):
        # Body Types: SUV, Hatchback, Sedan, Coupe, Convertible, Pickup, MUV, Crossover
        body_types = [
            'SUV', 'Hatchback', 'Sedan', 'Coupe', 
            'Convertible', 'Pickup', 'MUV', 'Crossover'
        ]
        
        fuels = ['Petrol', 'Diesel', 'Electric', 'Hybrid']
        transmissions = ['Manual', 'Automatic']
        
        brands_models = {
            'SUV': [
                ('Toyota', 'Fortuner', 'Legender'),
                ('Hyundai', 'Creta', 'SX(O)'),
                ('Mahindra', 'XUV700', 'AX7'),
                ('Tata', 'Safari', 'Dark Edition'),
                ('BMW', 'X5', 'M Sport')
            ],
            'Hatchback': [
                ('Maruti', 'Swift', 'ZXI+'),
                ('Hyundai', 'i20', 'Asta'),
                ('Tata', 'Altroz', 'XZ+'),
                ('Volkswagen', 'Polo', 'GT'),
                ('Toyota', 'Glanza', 'V')
            ],
            'Sedan': [
                ('Honda', 'City', 'ZX'),
                ('Hyundai', 'Verna', 'Turbo'),
                ('Skoda', 'Slavia', 'Style'),
                ('Volkswagen', 'Virtus', 'GT'),
                ('Mercedes-Benz', 'C-Class', 'C200')
            ],
            'Coupe': [
                ('Ford', 'Mustang', 'GT'),
                ('Porsche', '911', 'Carrera S'),
                ('Audi', 'RS5', 'Sportback'),
                ('BMW', '4 Series', 'M440i'),
                ('Jaguar', 'F-Type', 'R-Dynamic')
            ],
            'Convertible': [
                ('Mazda', 'MX-5', 'RF'),
                ('BMW', 'Z4', 'M40i'),
                ('Mini', 'Cooper', 'Convertible'),
                ('Mercedes-Benz', 'E-Class', 'Cabriolet'),
                ('Audi', 'A5', 'Cabriolet')
            ],
            'Pickup': [
                ('Isuzu', 'D-Max', 'V-Cross'),
                ('Toyota', 'Hilux', 'High'),
                ('Ford', 'Ranger', 'Raptor'),
                ('Jeep', 'Gladiator', 'Rubicon'),
                ('Chevrolet', 'Silverado', 'LTZ')
            ],
            'MUV': [
                ('Toyota', 'Innova Hycross', 'ZX'),
                ('Kia', 'Carens', 'Luxury Plus'),
                ('Maruti', 'Ertiga', 'ZXI+'),
                ('Renault', 'Triber', 'RXZ'),
                ('Mahindra', 'Marazzo', 'M6+')
            ],
            'Crossover': [
                ('Tata', 'Punch', 'Creative'),
                ('Citroen', 'C3', 'Shine'),
                ('Maruti', 'Fronx', 'Alpha'),
                ('Hyundai', 'Exter', 'SX'),
                ('Nissan', 'Magnite', 'XV Premium')
            ]
        }

        created_count = 0
        for b_type, vehicles in brands_models.items():
            self.stdout.write(f'Adding {b_type} vehicles...')
            for brand, model, variant in vehicles:
                price = Decimal(random.randint(10, 150)) * 100000 # 10L to 1.5Cr
                discount = random.choice([None, 5, 10, 15])
                offer_price = None
                if discount:
                    offer_price = price * (Decimal(100 - discount) / 100)
                
                v = Vehicle.objects.create(
                    brand=brand,
                    model=model,
                    variant=variant,
                    price=price,
                    discount_percentage=discount,
                    offer_price=offer_price,
                    fuel_type=random.choice(fuels),
                    transmission=random.choice(transmissions),
                    engine=f"{random.choice([1.2, 1.5, 2.0, 3.0, 4.0])}L Turbo",
                    mileage=Decimal(random.uniform(8, 25)).quantize(Decimal('0.00')),
                    seating_capacity=random.choice([2, 4, 5, 7]),
                    body_type=b_type,
                    color=random.choice(['Black', 'White', 'Silver', 'Blue', 'Red']),
                    description=f"Experience the peak of performance and luxury with the all-new {brand} {model}. Designed for those who demand excellence.",
                    is_featured=random.choice([True, False]),
                    safety_rating=Decimal(random.choice([3.5, 4.0, 4.5, 5.0])),
                    search_count=random.randint(100, 5000)
                )
                created_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {created_count} vehicles.'))
