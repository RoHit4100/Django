from django.db import models

# Create your models here.
class Expense(models.Model):
    # create required columns
    title = models.CharField(max_length=150)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return self.title