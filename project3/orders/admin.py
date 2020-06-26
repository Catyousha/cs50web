from django.contrib import admin

from .models import Pizza, Topping, Subs, AdditionalSubs, Pasta, Salads, DinnerPlatters
from .models import UserShoppingCart, UserOrderList
# Register your models here.

admin.site.register(Pizza)
admin.site.register(Topping)
admin.site.register(Subs)
admin.site.register(AdditionalSubs)
admin.site.register(Pasta)
admin.site.register(Salads)
admin.site.register(DinnerPlatters)

admin.site.register(UserShoppingCart)
admin.site.register(UserOrderList)
