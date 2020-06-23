from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User

from orders.models import Pizza, Topping, Subs, AdditionalSubs, Pasta, Salads, DinnerPlatters

# Create your views here.
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

    logout(request)
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

def menuList(request, menu_type="Regular"):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("login")

    menu_type = menu_type.replace("-"," ")
    menu_type = menu_type.title()

    if menu_type == "Regular" or menu_type == "Sicilian":
        menus = Pizza.objects.filter(category=menu_type)

    elif menu_type == "Subs":
        menus = Subs.objects.all()

    elif menu_type == "Pasta":
        menus = Pasta.objects.all()

    elif menu_type == "Salads":
        menus = Salads.objects.all()

    elif menu_type == "Dinner Platters":
        menus = DinnerPlatters.objects.all()

    else:
        menu_type = "Regular"
        menus = Pizza.objects.filter(category="Regular")

    return render(request, "order/menu_list.html", {'menus': menus, 'menu_type': menu_type})

def ordering(request, menu_type, menu_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("login")
    menu_type = menu_type.replace("-"," ")
    menu_type = menu_type.title()

    if menu_type == "Regular" or menu_type == "Sicilian":
        menus = Pizza.objects.filter(category=menu_type)
        try:
            menu = menus[menu_id-1]
        except Pizza.DoesNotExist:
            return HttpResponseRedirect(reverse("default menu list"))

        if "Topping" in menu.name:
            tops = {'type':"Topping", 'num':range(int(menu.name[0])) }
            tops_list = Topping.objects.all()
        elif "Item" in menu.name:
            tops = {'type':"Item", 'num':range(int(menu.name[0]))}
            tops_list = Topping.objects.all()
        else:
            tops = None
            tops_list = None
        return render(request, "order/ordering.html", {'menu':menu, 'menu_type':menu_type, 'tops':tops, 'tops_list': tops_list})

    elif menu_type == "Subs":
        menu = Subs.objects.get(pk=menu_id)

    elif menu_type == "Pasta":
        menu = Pasta.objects.get(pk=menu_id)

    elif menu_type == "Salads":
        menu = Salads.objects.get(pk=menu_id)

    elif menu_type == "Dinner Platters":
        menu = DinnerPlatters.objects.get(pk=menu_id)

    else:
        return HttpResponseRedirect(reverse("default menu list"))

    return render(request, "order/ordering.html", {'menu':menu, 'menu_type':menu_type})


def orderList(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    return render(request, "order/order_list.html")

def shoppingCart(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    return render(request, "order/shopping_cart.html")
