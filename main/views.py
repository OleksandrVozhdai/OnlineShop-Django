from django.http import HttpResponse
from django.shortcuts import render
from .models import TechList

# Create your views here.

def IndexView(request):
    return render(request, 'main/index.html')

def ShopView(request):
    products = TechList.objects.all()
    return render(request, 'main/shop.html', {'products': products})

def AboutView(request):
    return render(request, 'main/about.html')

def CatalogView(request):
    return render(request, 'main/catalog.html')

def SmartphonesView(request):
    smartphones = TechList.objects.filter(category="Smartphone")
    return render(request, 'main/smartphones.html', {"smartphones": smartphones})

def LaptopsView(request):
    laptops = TechList.objects.filter(category="Laptop")
    return render(request, 'main/laptops.html', {"laptops": laptops})

def MousesView(request):
    mouses = TechList.objects.filter(category="Mouse")
    return render(request, 'main/mouses.html', {"mouses": mouses})

def TelevisionsView(request):
    televisions = TechList.objects.filter(category="Television")
    return render(request, 'main/televisions.html', {"televisions": televisions})

def RegistrationView(request):
    return render(request, 'main/registration.html')

def LogInView(request):
    return render(request, 'main/login.html')