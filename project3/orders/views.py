from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return HttpResponse("Project 3: TODO")

def login(request):
    return render(request, "auth/login.html")

def register(request):
    return render(request, "auth/register.html")

def orderList(request):
    return render(request, "order/order_list.html")

def menuList(request):
    return render(request, "order/menu_list.html")

def shoppingCart(request):
    return render(request, "order/shopping_cart.html")
