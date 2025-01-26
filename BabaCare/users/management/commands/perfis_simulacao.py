import random, math
from math import radians, sin, cos, acos
from django.core.management.base import BaseCommand
from users.models import Baba

class Command(BaseCommand):
    help = "Create 20 random Baba profiles near -23.227777, -45.905624 within 50 km"

    def handle(self, *args, **options):
        center_lat = -23.227777
        center_lon = -45.905624
        radius_km = 10

        def random_location_in_radius(center_lat, center_lon, max_radius_km):
            # Convert max_radius_km to degrees (~111 km per degree latitude)
            max_radius_deg = max_radius_km / 111.0
            # Random distance in degrees
            r = max_radius_deg * math.sqrt(random.random())
            # Random angle
            theta = random.random() * 2 * math.pi

            delta_lat = r * math.cos(theta)
            delta_lon = r * math.sin(theta) / math.cos(radians(center_lat))

            return (center_lat + delta_lat, center_lon + delta_lon)

        for i in range(20):
            # Generate random lat/long within 50 km radius
            lat, lon = random_location_in_radius(center_lat, center_lon, radius_km)

            baba = Baba.objects.create_user(
                email=f"baba{i}@example.com",
                nome=f"Baba Random {i}",
                cpf=f"CPF{i:03d}",
                nascimento="1990-01-01",
                telefone="11999999999",
                endereco=f"Endereço {i}",
                numero=str(i),
                password="password123",
                isBaba=True
            )
            baba.bioBaba = f"Bio for Baba {i}"
            baba.habilidades = "Variadas"
            baba.rangeTrabalho = i
            baba.lat = lat
            baba.long = lon
            baba.save()

        self.stdout.write(self.style.SUCCESS('Successfully created 20 random Baba profiles.'))