from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def IndexView(request):
    return render(request, 'main/index.html')


def ShopView(request):
    return render(request, 'main/shop.html')


def AboutView(request):
    return render(request, 'main/about.html')


def CatalogView(request):
    return render(request, 'main/catalog.html')


def RegistrationView(request):
    return render(request, 'main/registration.html')


def LogInView(request):
    return render(request, 'main/login.html')


