from django.shortcuts import render

def home(request):
    return render(request, "home.html")

def login_page(request):
    return render(request, "login.html")

def orders_page(request):
    return render(request, "orders.html")
