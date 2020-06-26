from django.db import models
from django.contrib.auth.models import User

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

class UserShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shoppingcart") #user
    user_fullname = models.CharField(max_length=255) #Awanama Wijaya
    menu_desc = models.CharField(max_length=255) #Regular Pizza: Cheese
    menu_portion=models.CharField(max_length=32) #Small
    price = models.DecimalField(max_digits=4, blank=True, decimal_places=2, null=True) #6.00
    topping1 = models.CharField(max_length=32, null=True, blank=True)
    topping2 = models.CharField(max_length=32, null=True, blank=True)
    topping3 = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return f"{self.user_fullname}: {self.menu_desc} [{self.menu_portion}] ${self.price} [Toppings: {self.topping1}, {self.topping2}, {self.topping3}]"

class UserOrderList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders") #user
    user_fullname = models.CharField(max_length=255) #Awanama Wijaya
    order_desc = models.TextField() #Regular Pizza: 3 Toppings [Pepperoni, Anchovies, Chicken Berbecue]; Subs: etc...
    total_price = models.DecimalField(max_digits=4, blank=True, decimal_places=2, null=True) #37.70
    user_address = models.TextField()

    ORDER_STATUS_CHOICES = (
        ('1', 'Waiting'),
        ('2', 'Cooking'),
        ('3', 'Delivering'),
        ('4', 'Complete')
    )
    order_status = models.CharField(max_length=1, choices=ORDER_STATUS_CHOICES)
    def __str__(self):
        return f"{self.user_fullname}: {self.order_desc} [{self.order_status}] ${self.total_price} [Address: {self.user_address}]"
