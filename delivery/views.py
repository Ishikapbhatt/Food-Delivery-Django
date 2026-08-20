from django.shortcuts import render, get_object_or_404
from restaurants.models import Restaurant

def home(request):
    return render(request, "home.html")

def login_page(request):
    return render(request, "login.html")

def orders_page(request):
    return render(request, "orders.html")

def restaurants_page(request):
    return render(request, "restaurants.html")

def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id, is_active=True)
    return render(request, "restaurant_detail.html", {'restaurant_id': restaurant_id})

def cart_page(request):
    return render(request, "cart.html")
