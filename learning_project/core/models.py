from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
# Restaurant
from django.db import models
from datetime import datetime

from django.db import models
from datetime import datetime

class Restaurant(models.Model):
    RESTAURANT_TYPE_CHOICES = [
        ('IN', "Indian"),
        ('IT', "Italian"),
        ('CH', "Chinese"),
        ('JP', "Japanese"),
        ('MX', "Mexican"),
        ('FR', "French"),
        ('US', "American"),
        ('MD', "Mediterranean"),
        ('TH', "Thai"),
        ('GR', "Greek"),
        ('OTH', 'Other')
    ]

    name = models.CharField(max_length=100, db_index=True)
    website = models.URLField(default='')
    date_opened = models.DateField(default=datetime.today)
    longitude = models.FloatField()
    latitude = models.FloatField()
    restaurant_type = models.CharField(max_length=3, choices=RESTAURANT_TYPE_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.restaurant_type})"


# User, by default provided model
# Rating
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="visited_users")
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, db_index=True, related_name="ratings")
    rating = models.SmallIntegerField()
    review = models.TextField()
    
    
    class Meta:
        indexes = [
            models.Index(fields=['user', 'restaurant']),  # Composite index for user and restaurant
        ]
    
    def __str__(self):
        return f'{self.user}, has given {self.rating} to {self.restaurant}'


# Sale
class Sale(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True, related_name="sales")
    income = models.DecimalField(max_digits=10, decimal_places=2)
    date_time = models.DateTimeField()
