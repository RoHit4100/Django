from django.db import models

# Create your models here.
class Expense(models.Model):
    # here I will define the schema or model
    title = models.CharField(max_length=50)
    amount = models.IntegerField()
    date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
    
    