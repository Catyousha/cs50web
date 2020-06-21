from django.urls import path

from . import views

urlpatterns = [
    path("menu-list", views.menuList, name="menu list"),
    path("order-list", views.orderList, name="order list"),
    path("shopping-cart", views.shoppingCart, name="shopping cart"),
    path("login", views.login, name="login"),
    path("register", views.register, name="register"),
]
