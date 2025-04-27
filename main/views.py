from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth import login
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserRegistrationForm, UserLoginForm
from .models import TechList, User
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
import random

def IndexView(request):
    return render(request, 'main/index.html')


def ProductPageView(request, id):
    product = get_object_or_404(TechList, id=id)
    all_products = TechList.objects.all()
    constAllProducts = random.sample(list(all_products), min(6, len(all_products)))

    relatedProducts = TechList.objects.filter(category=product.category).exclude(id=product.id)
    sameBrandProducts = TechList.objects.filter(brand=product.brand).exclude(id=product.id)[:6]

    return render(request, 'main/productPage.html', {
        'product': product,
        'relatedProducts': relatedProducts,
        'sameBrandProducts': sameBrandProducts,
        'constAllProducts' : constAllProducts,
    })



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

    isOnSale = products.filter(on_sale=True)

    brands = TechList.objects.values_list('brand', flat=True).distinct()
    categories = TechList.objects.values_list('category', flat=True).distinct()

    return render(request, 'main/shop.html', {
        'products': products,
        'brands': brands,
        'categories': categories,
        'is_filtered': is_filtered,
        'isOnSale': isOnSale,

    })

def AboutView(request):
    return render(request, 'main/about.html')

def CatalogView(request):
    return render(request, 'main/catalog.html')


# Registration
def RegistrationView(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # user deactivation to confirm email
            user.save()

            # sent email
            subject = 'Confirm Your Registration at DeviceMarket'
            message = f'Hello, {user.full_name}!\n\nThank you for registering. Please click the link below to activate your account:\nhttp://{request.get_host()}/activate/{user.id}/'
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

            return redirect('main:login')  # redirecting
    else:
        form = UserRegistrationForm()
    return render(request, 'main/registration.html', {'form': form})

# Account Activation
def ActivateView(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.is_active = True
        user.save()
        return redirect('main:login')
    except User.DoesNotExist:
        return render(request, 'main/error.html', {'message': 'User not found'})

# LogIn
class LogInView(AuthLoginView):
    form_class = UserLoginForm
    template_name = 'main/login.html'