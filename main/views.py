from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import TechList
from django.http import JsonResponse

# Create your views here.

def IndexView(request):
    return render(request, 'main/index.html')

def ShopView(request):
    products = TechList.objects.all()
    is_filtered = False

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
        is_filtered = True
    if max_price:
        products = products.filter(price__lte=max_price)
        is_filtered = True

    brand = request.GET.get('brand')
    if brand:
        products = products.filter(brand=brand)
        is_filtered = True

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

def ProductPageView(request, id):
    product = get_object_or_404(TechList, id=id)
    relatedProducts = TechList.objects.filter(category= product.category)
    return render(request, 'main/productPage.html', {'product': product, 'relatedProducts': relatedProducts})

def Toggle_wishlist(request, id):
    if request.method == 'POST':
        product = get_object_or_404(TechList, id=id)
        product.on_wishlist = not product.on_wishlist
        product.save()
        return JsonResponse({'success': True, 'on_wishlist': product.on_wishlist})
    return JsonResponse({'success': False})

def WishlistView(request):
    wishlistProducts = TechList.objects.filter(on_wishlist=True)
    return render(request, 'main/wishlist.html', {"wishlistProducts": wishlistProducts})

def RegistrationView(request):
    return render(request, 'main/registration.html')

def LogInView(request):
    return render(request, 'main/login.html')