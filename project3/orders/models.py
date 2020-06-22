from django.db import models

# Create your models here.
class Pizza(models.Model):
    category = models.CharField(max_length=16) #Regular or Sicilian
    name = models.CharField(max_length=64) #Cheese
    small = models.DecimalField(max_digits=4, decimal_places=2, null=True) #12.70
    big = models.DecimalField(max_digits=4, decimal_places=2, null=True) #17.95
    picture = models.CharField(max_length=255) #image links

    def __str__(self):
        return f"{self.name}: [Small: {self.small}] [Big: {self.big}]"

class Topping(models.Model):
    name = models.CharField(max_length=32)
    pizza = models.ManyToManyField(Pizza, blank=True, related_name="toppings")

    def __str__(self):
        return f"{self.name}"
