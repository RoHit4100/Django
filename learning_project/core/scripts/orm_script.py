from ..models import Restaurant
from datetime import datetime

def run():
    restaurant = Restaurant()
    restaurant.name = 'Hotel EverShine'
    restaurant.latitude = 50.12
    restaurant.longitude = 60.1
    restaurant.restaurant_type = 'IN'
    restaurant.date_opened = datetime.today()  # Set the date_opened
    restaurant.website = 'https://example.com'  # Set the website to a default value

    restaurant.save()
