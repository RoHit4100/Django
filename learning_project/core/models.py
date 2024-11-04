from django.core.validators import MaxValueValidator, MinValueValidator, URLValidator, RegexValidator
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .constants import RESTAURANT_TYPE_CHOICES

# Restaurant
class Restaurant(models.Model):
    name = models.CharField(
        max_length=100,
        db_index=True,
        validators=[
            RegexValidator(r'^[A-Za-z ]+$', message="Name should contain only letters and spaces.")
        ]
    )
    website = models.URLField(default='', validators=[URLValidator()])
    date_opened = models.DateField(default=timezone.now)
    longitude = models.FloatField(validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)])
    latitude = models.FloatField(validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)])
    restaurant_type = models.CharField(max_length=3, choices=RESTAURANT_TYPE_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.restaurant_type})"
    
    def save(self, *args, **kwargs):
        self.full_clean()  # Run validators
        super(Restaurant, self).save(*args, **kwargs)


# Rating
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="visited_users")
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, db_index=True, related_name="ratings")
    rating = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])  # Restrict rating to 1-5
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

    def __str__(self):
        return f"Sale of {self.income} at {self.restaurant} on {self.date_time}"
