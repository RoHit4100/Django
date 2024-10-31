from ..models import Restaurant, User, Rating, Sale  # Ensure to import your models correctly
from faker import Faker
import random
from django.utils import timezone
from django.db import connection



def run():
    fake = Faker()
    
    # Function to insert values into the restaurant
    def create_restaurants(count):
        types = [
            'IN',  # Indian
            'IT',  # Italian
            'CH',  # Chinese
            'JP',  # Japanese
            'MX',  # Mexican
            'FR',  # French
            'US',  # American
            'MD',  # Mediterranean
            'TH',  # Thai
            'GR',  # Greek
            'OTH'  # Other
        ]

        for _ in range(count):
            restaurant = Restaurant()
            restaurant.name = fake.company()
            restaurant.latitude = fake.latitude()
            restaurant.longitude = fake.longitude()
            restaurant.restaurant_type = random.choice(types)
            restaurant.date_opened = fake.date_this_decade()  # Set the date_opened
            restaurant.website = fake.url()  # Set the website
            restaurant.save()

    create_restaurants(100)
    # print(connection.queries)
    
    # Function to create users 
    def create_users(count):
        for _ in range(count):
            user = User()
            user.username = fake.user_name()
            user.password = fake.password()
            user.email = fake.email()
            user.save()
        
    create_users(10)
    
    # Function to create ratings
    def create_ratings(count):
        users = User.objects.all()
        restaurants = Restaurant.objects.all()
        
        for _ in range(count):
            rating = Rating()
            rating.user = random.choice(users)
            rating.restaurant = random.choice(restaurants)   
            rating.rating = random.randint(0, 5)
            rating.review = fake.text()
            rating.save()  # Save the rating to the database

    create_ratings(50)
    
    # Function to create sales for the restaurants
    def create_sales(count):
        restaurants = Restaurant.objects.all()
        for _ in range(count):
            sale = Sale()
            sale.restaurant = random.choice(restaurants)
            sale.income = round(random.uniform(100, 100000000), 2)

            # Generate a naive datetime and make it timezone aware
            naive_datetime = fake.date_time_this_decade()  # This generates a naive datetime
            sale.date_time = timezone.make_aware(naive_datetime)  # Convert to timezone-aware datetime
            
            sale.save()  # Save the sale to the database

    create_sales(100)