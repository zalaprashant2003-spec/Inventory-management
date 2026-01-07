from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .forms import NewUserForm, ItemForm, OrderForm
from .models import Item, Order
import datetime

def home(request):
    context = {"dataset": Item.objects.all()}
    return render(request, 'home.html')

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("firstapp:home")
        else:
            messages.error(request, "Unsuccessful registration. Please correct the errors below.")
    else:
        form = NewUserForm()
    return render(request, "register.html", {"register_form": form})

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("firstapp:home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, "login.html", {"login_form": form})

def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("firstapp:home")


def create_item(request):
    form = ItemForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('firstapp:list_item')
    return render(request, "create_item.html", {"form": form})

def list_item(request):
    context = {"dataset": Item.objects.all()}
    return render(request, "list_item.html", context)

def list_customer(request):
    context = {"dataset": User.objects.all()}
    return render(request, "list_customer.html", context)

def item_less_than(request):
    context = {"dataset": Item.objects.filter(quantity__lt=10)}
    return render(request, "item_less_than.html", context)

def detail_item(request, id):
    context = {"data": Item.objects.get(id=id)}
    return render(request, "detail_item.html", context)

def update_item(request, id):
    obj = get_object_or_404(Item, id=id)
    form = ItemForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect("firstapp:list_item")
    return render(request, "update_item.html", {"form": form})

def delete_item(request, id):
    obj = get_object_or_404(Item, id=id)
    if request.method == "POST":
        obj.delete()
        return redirect("firstapp:list_item")    
    return render(request, "delete_item.html", {"item": obj})

def bill(request, customer):
    user = get_object_or_404(User, username=customer)
    orders = Order.objects.filter(customer=user, order_date=datetime.date.today())
    total_amount = sum(order.quantity * order.item.price for order in orders)
    return render(request, "bill.html", {"data": orders, "total_amount": total_amount})

def alltime_purchase(request, customer):
    user = get_object_or_404(User, username=customer)
    orders = Order.objects.filter(customer=user)
    return render(request, "alltime_purchase.html", {"data": orders})

# def create_order(request):
#     form = OrderForm(request.POST or None)
#     if form.is_valid():
#         order = form.save(commit=False)
#         order.customer = request.user
#         item = get_object_or_404(Item, id=order.item.id)
#         if item.quantity >= order.quantity:
#             item.quantity -= order.quantity
#             item.save()
#             order.save()
#             return redirect("firstapp:home")
#         else:
#             return render(request, "create_order.html", {"form": form, "error": "Not enough stock available!"})
#     return render(request, "create_order.html", {"form": form})


def add(request):
    val1 = request.POST['num1']
    return render(request, 'result.html', {'result': val1})
def sub(request):
    val1 = request.POST['num1']
    context = {  # Initialize context before using it
        "data": User.objects.filter(username__startswith=val1)
    }
    return render(request, 'home.html', context)

def lit_customer(request) : 
    context={}
    context["dataset"]=User.objects.all()
    return render(request,"list_customer.html",context)


def order_page(request):
    items = Item.objects.all()
    cart = request.session.get('cart', {})

    cart_items = []
    for item_id, quantity in cart.items():
        item = get_object_or_404(Item, id=item_id)
        cart_items.append({'item': item, 'quantity': quantity})

    return render(request, "order_page.html", {"items": items, "cart_items": cart_items})

def add_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    cart = request.session.get('cart', {})

    if str(item_id) in cart:
        cart[str(item_id)] += 1
    else:
        cart[str(item_id)] = 1

    request.session['cart'] = cart
    return redirect("firstapp:order_page")

def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})
    
    if str(item_id) in cart:
        del cart[str(item_id)]
    
    request.session['cart'] = cart
    return redirect("firstapp:order_page")

def update_cart(request):
    if request.method == "POST":
        cart = request.session.get('cart', {})
        
        for key in request.POST:
            if key.startswith("quantity_"):
                item_id = key.split("_")[1]
                quantity = int(request.POST[key])
                
                item = get_object_or_404(Item, id=item_id)
                if quantity > item.quantity:
                    messages.error(request, f"Not enough stock for {item.item_name}.")
                elif quantity < 1:
                    cart.pop(item_id, None)
                else:
                    cart[item_id] = quantity

        request.session['cart'] = cart
        return redirect("firstapp:order_page")

def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect("firstapp:order_page")

    user = request.user
    total_amount = 0
    orders = []

    for item_id, quantity in cart.items():
        item = get_object_or_404(Item, id=item_id)
        if item.quantity >= quantity:
            item.quantity -= quantity
            item.save()
            order = Order.objects.create(customer=user, item=item, quantity=quantity)
            orders.append(order)
            total_amount += quantity * item.price

    request.session["cart"] = {}

    return redirect("firstapp:customer_bill")  

    

def customer_bill(request):
    user = request.user
    today = datetime.date.today()
    orders = Order.objects.filter(customer=user, order_date=today)
    total_amount = sum(order.quantity * order.item.price for order in orders)

    return render(request, "customer_bill.html", {"orders": orders, "total_amount": total_amount})


def customer_alltime(request):
    user = request.user
    orders = Order.objects.filter(customer=user).order_by("-order_date")

    total_amount = sum(order.quantity * order.item.price for order in orders)

    return render(request, "customer_alltime.html", {"orders": orders, "total_amount": total_amount})
