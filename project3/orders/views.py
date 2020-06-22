from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    return HttpResponse("Project 3: TODO")

def loginView(request):
    if request.method == "POST":
        username = request.POST["username"]
        pass1 = request.POST["pass"]
        user = authenticate(request, username=username, password=pass1)
        if user is None:
            login(request, "auth/login.html", {'message': "Invalid Credentials"})
        else:
            login(request, user)
            return HttpResponseRedirect(reverse("menu list"))
    if request.session.get('firstlogin') is not None:
        msg = request.session.get('firstlogin')
        del request.session['firstlogin']
        return render(request, "auth/login.html", {'message': msg})
    return render(request, "auth/login.html")

def registerView(request):
    if request.method == "POST":
        pass1 = request.POST["pass"]
        pass2 = request.POST["pass2"]
        if pass1 != pass2:
            return render(request, "auth/register.html", {'message':"Password didn't match!"})

        first_name = request.POST["fname"]
        last_name = request.POST["lname"]
        username = request.POST["username"]
        email = request.POST["email"]
        user = User.objects.create_user(username, email, pass1)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        request.session["firstlogin"] = "Registration success, you can login now."

        return HttpResponseRedirect(reverse("login"))

    return render(request, "auth/register.html")

def orderList(request):
    return render(request, "order/order_list.html")

def menuList(request):
    return render(request, "order/menu_list.html")

def shoppingCart(request):
    return render(request, "order/shopping_cart.html")
