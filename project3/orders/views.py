from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User

from orders.models import Pizza, Topping, Subs, AdditionalSubs, Pasta, Salads, DinnerPlatters
from orders.models import UserShoppingCart

from django.db.models import Sum

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
            return HttpResponseRedirect(reverse("default menu list"))
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

    if request.method == "POST":
        menu_desc = request.POST.get("menu", False) #Regular Pizza: Cheese
        price_type = request.POST.get("price_type") #Small-5.00
        if "Normal" in price_type:
            price = float(price_type.replace("Normal-",""))
            menu_portion = "Normal"
        elif "Small" in price_type:
            price = float(price_type.replace("Small-",""))
            menu_portion = "Small"
        elif "Big" in price_type:
            price = float(price_type.replace("Big-",""))
            menu_portion = "Big"

        topping1 = request.POST.get("topping1")
        if topping1 is not None:
            topping1 = topping1.replace("-"," ").title()

        topping2 = request.POST.get("topping2")
        if topping2 is not None:
            topping2 = topping2.replace("-"," ").title()

        topping3 = request.POST.get("topping3")
        if topping3 is not None:
            topping3 = topping3.replace("-"," ").title()

        adds = request.POST.getlist("adds", False)
        if adds is not False:
            menu_desc = menu_desc + " (" #Subs: Cheese (
            for add in adds:
                add = add.split('-')
                menu_desc = menu_desc + " " + add[0] #Subs: Hamburger + Mushroom
                price = price + float(add[1])
            menu_desc = menu_desc + ")" #Subs: Cheese (+ Mushroom)

        UserShoppingCart(user=request.user,
                        user_fullname=request.user.first_name + " " +request.user.last_name,
                        menu_desc=menu_desc,
                        price=price,
                        menu_portion=menu_portion,
                        topping1=topping1,
                        topping2=topping2,
                        topping3=topping3).save()
        return HttpResponseRedirect(reverse("shopping cart"))


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
        return render(request, "order/ordering.html", {'menu':menu, 'menu_type':menu_type+' Pizza', 'tops':tops, 'tops_list': tops_list})

    elif menu_type == "Subs":
        menu = Subs.objects.get(pk=menu_id)
        tops = {'type':"Adds", 'num':range(1) }
        tops_list = AdditionalSubs.objects.all()
        return render(request, "order/ordering.html", {'menu':menu, 'menu_type':menu_type, 'tops':tops, 'tops_list': tops_list})

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

    carts = request.user.shoppingcart.all()
    if carts:
        total_price = round(request.user.shoppingcart.all().aggregate(Sum('price'))['price__sum'], 2)
    else:
        total_price = None
    return render(request, "order/shopping_cart.html", {'carts':carts, 'total_price':total_price})
