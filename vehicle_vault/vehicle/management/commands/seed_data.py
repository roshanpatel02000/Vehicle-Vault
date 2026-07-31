from django.core.management.base import BaseCommand
from vehicle.models import Vehicle
from accessory.models import Accessory, VehicleAccessoryMap

class Command(BaseCommand):
    help = 'Seeds initial vehicle and accessory data if database is empty.'

    def handle(self, *args, **kwargs):
        if Vehicle.objects.count() > 0:
            self.stdout.write(self.style.SUCCESS("Database already contains vehicle data. Skipping seed."))
            return

        self.stdout.write("Seeding sample vehicles and accessories...")

        vehicles_data = [
            {
                'brand': 'Tesla',
                'model': 'Model 3',
                'variant': 'Long Range AWD',
                'price': 47990.00,
                'discount_percentage': 5,
                'offer_price': 45590.00,
                'fuel_type': 'Electric',
                'transmission': 'Automatic',
                'engine': 'Dual Motor Electric',
                'mileage': 341.00,  # Range in miles
                'seating_capacity': 5,
                'body_type': 'Sedan',
                'color': 'Pearl White Multi-Coat',
                'description': 'The Tesla Model 3 offers quick acceleration, long battery range, and cutting-edge Autopilot features in a sleek electric sedan.',
                'image_url': 'https://images.unsplash.com/photo-1560958089-b8a1929cea89?w=800',
                'is_featured': True,
                'safety_rating': 5.0,
                'search_count': 142,
            },
            {
                'brand': 'BMW',
                'model': 'M4 Competition',
                'variant': 'Coupe xDrive',
                'price': 79100.00,
                'discount_percentage': 4,
                'offer_price': 75936.00,
                'fuel_type': 'Petrol',
                'transmission': 'Automatic',
                'engine': '3.0L M TwinPower Turbo I6',
                'mileage': 23.00,
                'seating_capacity': 4,
                'body_type': 'Coupe',
                'color': 'Isle of Man Green',
                'description': 'Aggressive styling paired with 503 horsepower makes the BMW M4 Competition the ultimate track-ready high-performance luxury coupe.',
                'image_url': 'https://images.unsplash.com/photo-1555215695-3004980ad54e?w=800',
                'is_featured': True,
                'safety_rating': 4.8,
                'search_count': 189,
            },
            {
                'brand': 'Porsche',
                'model': 'Taycan',
                'variant': 'Turbo S',
                'price': 185000.00,
                'discount_percentage': 3,
                'offer_price': 179450.00,
                'fuel_type': 'Electric',
                'transmission': 'Automatic',
                'engine': 'Permanent Magnet Synchronous',
                'mileage': 278.00,
                'seating_capacity': 4,
                'body_type': 'Sedan',
                'color': 'Frozen Blue Metallic',
                'description': 'Pure Porsche sports car DNA combined with electric performance. 750 horsepower overboost launches from 0 to 60 mph in 2.6 seconds.',
                'image_url': 'https://images.unsplash.com/photo-1614162692292-7ac56d7f7f1e?w=800',
                'is_featured': True,
                'safety_rating': 5.0,
                'search_count': 210,
            },
            {
                'brand': 'Mercedes-Benz',
                'model': 'C-Class',
                'variant': 'C 300 Sedan',
                'price': 44850.00,
                'discount_percentage': 6,
                'offer_price': 42159.00,
                'fuel_type': 'Hybrid',
                'transmission': 'Automatic',
                'engine': '2.0L Turbo I4 with Mild Hybrid',
                'mileage': 35.00,
                'seating_capacity': 5,
                'body_type': 'Sedan',
                'color': 'Obsidian Black Metallic',
                'description': 'Elevated luxury with MBUX touchscreen infotainment, ambient lighting, and smooth mild-hybrid efficiency.',
                'image_url': 'https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=800',
                'is_featured': False,
                'safety_rating': 4.9,
                'search_count': 95,
            },
            {
                'brand': 'Audi',
                'model': 'e-tron GT',
                'variant': 'RS Quattro',
                'price': 106500.00,
                'discount_percentage': 5,
                'offer_price': 101175.00,
                'fuel_type': 'Electric',
                'transmission': 'Automatic',
                'engine': 'Dual Electric Motors',
                'mileage': 249.00,
                'seating_capacity': 5,
                'body_type': 'Sedan',
                'color': 'Daytona Gray Pearl',
                'description': 'A breathtaking electric grand tourer featuring Quattro all-wheel drive, air suspension, and ultra-fast 800V charging capability.',
                'image_url': 'https://images.unsplash.com/photo-1603584173870-7f23fdae1b7a?w=800',
                'is_featured': True,
                'safety_rating': 5.0,
                'search_count': 167,
            },
            {
                'brand': 'Ford',
                'model': 'Mustang',
                'variant': 'GT Fastback',
                'price': 42495.00,
                'discount_percentage': 8,
                'offer_price': 39095.00,
                'fuel_type': 'Petrol',
                'transmission': 'Manual',
                'engine': '5.0L Ti-VCT V8',
                'mileage': 24.00,
                'seating_capacity': 4,
                'body_type': 'Coupe',
                'color': 'Grabber Blue Metallic',
                'description': 'Raw American muscle powered by a roaring 486 horsepower naturally-aspirated 5.0L Coyote V8 engine.',
                'image_url': 'https://images.unsplash.com/photo-1584345604476-8ec5e12e42dd?w=800',
                'is_featured': False,
                'safety_rating': 4.7,
                'search_count': 130,
            },
            {
                'brand': 'Land Rover',
                'model': 'Range Rover Sport',
                'variant': 'Dynamic SE',
                'price': 83600.00,
                'discount_percentage': 3,
                'offer_price': 81092.00,
                'fuel_type': 'Hybrid',
                'transmission': 'Automatic',
                'engine': '3.0L Turbocharged I6 MHEV',
                'mileage': 26.00,
                'seating_capacity': 5,
                'body_type': 'SUV',
                'color': 'Carpathian Grey',
                'description': 'Unmatched off-road capability fused with supreme luxury, terrain response control, and panoramic glass roof.',
                'image_url': 'https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?w=800',
                'is_featured': True,
                'safety_rating': 4.9,
                'search_count': 175,
            },
            {
                'brand': 'Hyundai',
                'model': 'Ioniq 5',
                'variant': 'Limited AWD',
                'price': 41450.00,
                'discount_percentage': 7,
                'offer_price': 38548.00,
                'fuel_type': 'Electric',
                'transmission': 'Automatic',
                'engine': 'Dual Electric Motor AWD',
                'mileage': 303.00,
                'seating_capacity': 5,
                'body_type': 'Crossover',
                'color': 'Gravity Gold Matte',
                'description': 'Retro-futuristic parametric pixel design, 800V ultra-fast charging, and ultra-spacious flat-floor cabin interior.',
                'image_url': 'https://images.unsplash.com/photo-1617788138017-80ad40651399?w=800',
                'is_featured': True,
                'safety_rating': 5.0,
                'search_count': 115,
            },
        ]

        created_vehicles = []
        for vdata in vehicles_data:
            v = Vehicle.objects.create(**vdata)
            created_vehicles.append(v)

        self.stdout.write(self.style.SUCCESS(f"Successfully created {len(created_vehicles)} vehicles."))

        accessories_data = [
            {
                'accessory_name': 'All-Weather Floor Mats Kit',
                'vehicle_type': 'Sedan',
                'brand': 'WeatherTech',
                'price': 149.99,
                'description': 'Heavy-duty laser-measured rubber floor liners designed to shield against dirt, mud, and water spills.',
                'availability': True,
            },
            {
                'accessory_name': 'Panoramic Sunroof Wind Deflector',
                'vehicle_type': 'SUV',
                'brand': 'Thule',
                'price': 89.50,
                'description': 'Reduces cabin wind noise and turbulence during highway driving with panoramic sunroof open.',
                'availability': True,
            },
            {
                'accessory_name': 'Fast Wireless Charging Phone Mount',
                'vehicle_type': 'Sedan',
                'brand': 'Anker',
                'price': 49.99,
                'description': '15W MagSafe compatible wireless charging phone holder with automatic sensor clamp.',
                'availability': True,
            },
            {
                'accessory_name': '4K Dual Dash Cam Front & Rear',
                'vehicle_type': 'SUV',
                'brand': 'Garmin',
                'price': 229.00,
                'description': 'Ultra-HD 4K night vision camera recording with GPS logging and 24/7 motion sensor parking mode.',
                'availability': True,
            },
            {
                'accessory_name': 'Custom Perforated Leather Seat Covers',
                'vehicle_type': 'Coupe',
                'brand': 'AutoStyle',
                'price': 299.99,
                'description': 'Breathable custom-fit premium Nappa leather seat covers with memory foam cushion pads.',
                'availability': True,
            },
            {
                'accessory_name': 'Smart Multi-Color Ambient LED Lighting',
                'vehicle_type': 'Crossover',
                'brand': 'Govee',
                'price': 39.99,
                'description': '64-color smartphone app controlled interior light strips with music sync mode.',
                'availability': True,
            },
        ]

        created_accessories = []
        for adata in accessories_data:
            a = Accessory.objects.create(**adata)
            created_accessories.append(a)

        self.stdout.write(self.style.SUCCESS(f"Successfully created {len(created_accessories)} accessories."))

        # Map accessories to vehicles
        for v in created_vehicles:
            for a in created_accessories:
                if a.vehicle_type.lower() in [v.body_type.lower() if v.body_type else '', 'sedan', 'suv']:
                    VehicleAccessoryMap.objects.get_or_create(vehicle=v, accessory=a)

        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))
