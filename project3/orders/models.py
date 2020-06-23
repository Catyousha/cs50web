from django.db import models

# Create your models here.
class Pizza(models.Model):
    category = models.CharField(max_length=16) #Regular or Sicilian
    name = models.CharField(max_length=64) #Cheese
    small = models.DecimalField(max_digits=4, blank=True, decimal_places=2, null=True) #12.70
    large = models.DecimalField(max_digits=4, blank=True, decimal_places=2, null=True) #17.95
    picture = models.CharField(max_length=255) #image links

    def __str__(self):
        return f"{self.name}: [Small: {self.small}] [large: {self.large}]"

class Topping(models.Model):
    name = models.CharField(max_length=32)
    pizza = models.ManyToManyField(Pizza, blank=True, related_name="toppings")

    def __str__(self):
        return f"{self.name}"

class Subs(models.Model):
    name = models.CharField(max_length=64) #Italian
    small = models.DecimalField(max_digits=4, blank=True, decimal_places=2, null=True) #6.50
    large = models.DecimalField(max_digits=4, blank=True, decimal_places=2, null=True) #7.95
    picture = models.CharField(max_length=255) #image links

    def __str__(self):
        return f"{self.name}: [Small: {self.small}] [large: {self.large}]"

class AdditionalSubs(models.Model):
    name = models.CharField(max_length=64)
    subs = models.ManyToManyField(Subs, blank=True, related_name="additional")
    small = models.DecimalField(max_digits=4, blank=True, decimal_places=2, null=True)
    large = models.DecimalField(max_digits=4, blank=True, decimal_places=2, null=True)

    def __str__(self):
        return f"{self.name}"

class Pasta(models.Model):
    name = models.CharField(max_length=64) #Baked Ziti
    price = models.DecimalField(max_digits=4, blank=True, decimal_places=2, null=True) #6.50
    picture = models.CharField(max_length=255) #image links

    def __str__(self):
        return f"{self.name} : {self.price}"

class Salads(models.Model):
    name = models.CharField(max_length=64) #Garden Salad
    price = models.DecimalField(max_digits=4, blank=True, decimal_places=2, null=True) #6.25
    picture = models.CharField(max_length=255) #image links

    def __str__(self):
        return f"{self.name} : {self.price}"

class DinnerPlatters(models.Model):
    name = models.CharField(max_length=64) #Greek Salad
    small = models.DecimalField(max_digits=4, blank=True, decimal_places=2, null=True) #50.00
    large = models.DecimalField(max_digits=4, blank=True, decimal_places=2, null=True) #75.00
    picture = models.CharField(max_length=255) #image links

    def __str__(self):
        return f"{self.name}: [Small: {self.small}] [large: {self.large}]"
