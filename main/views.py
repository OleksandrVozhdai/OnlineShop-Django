from django.http import HttpResponse
from django.shortcuts import render
from .models import TechList

# Create your views here.

# Представлення для головної сторінки
def IndexView(request):
    return render(request, 'main/index.html')

def ShopView(request):
    products = TechList.objects.all()
    is_filtered = False

    # Фільтрація за ціною
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
        is_filtered = True
    if max_price:
        products = products.filter(price__lte=max_price)
        is_filtered = True

    # Фільтрація за брендом
    brand = request.GET.get('brand')
    if brand:
        products = products.filter(brand=brand)
        is_filtered = True

    # Фільтрація за категорією
    category = request.GET.get('category')
    if category:
        products = products.filter(category=category)
        is_filtered = True

    brands = TechList.objects.values_list('brand', flat=True).distinct()
    categories = TechList.objects.values_list('category', flat=True).distinct()

    return render(request, 'main/shop.html', {
        'products': products,
        'brands': brands,
        'categories': categories,
        'is_filtered': is_filtered,
    })


# Представлення для сторінки "Про насasc
def AboutView(request):
    return render(request, 'main/about.html')


# Представлення для каталогу
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