from django.urls import path

from . import views

urlpatterns = [
    path("order-list", views.orderList, name="order list"),
    path("order/<slug:menu_type>/<int:menu_id>", views.ordering, name="ordering"),

    path("shopping-cart", views.shoppingCart, name="shopping cart"),
    path("shopping-cart/<slug:option>/<int:shopping_cart_id>", views.shoppingCart, name="shopping cart option"),
    
    path("login", views.loginView, name="login"),
    path("register", views.registerView, name="register"),

    path("",views.menuList, name="default menu list"),
    path("<slug:menu_type>", views.menuList, name="menu list"),
]
