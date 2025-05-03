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
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from .forms import UserRegistrationForm, UserLoginForm
from .models import TechList, User, PendingUser
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from decimal import Decimal


# Представлення для головної сторінки
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


def WishlistView(request, id):
    product = get_object_or_404(TechList, id=id)
    all_products = TechList.objects.all()
    constAllProducts = random.sample(list(all_products), min(6, len(all_products)))
    wishlistProducts = TechList.objects.filter(on_wishlist=True)

    return render(request, 'main/wishlist.html', {
        'wishlistProducts': wishlistProducts,
        'product': product,
        'constAllProducts' : constAllProducts,})

def ShopView(request):
    products = TechList.objects.all()

    is_filtered = False


# Представлення для магазину з фільтрацією товарів
def ShopView(request):
    products = TechList.objects.all()  # Отримуємо всі товари
    is_filtered = False  # Прапорець для перевірки, чи застосовані фільтри

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

    rating = request.GET.get('rating')
    if rating:
        products = products.filter(stars__gte=Decimal(rating))


    isOnSale = products.filter(on_sale=True)


    # Отримуємо унікальні бренди та категорії для фільтрів

    brands = TechList.objects.values_list('brand', flat=True).distinct()
    categories = TechList.objects.values_list('category', flat=True).distinct()

    return render(request, 'main/shop.html', {
        'products': products,
        'brands': brands,
        'categories': categories,
        'is_filtered': is_filtered,
        'isOnSale': isOnSale,

    })

# Представлення для сторінки "Про насasc
def AboutView(request):
    return render(request, 'main/about.html')


# Представлення для каталогу
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


# Представлення для смартфонів
def SmartphonesView(request):
    smartphones = TechList.objects.filter(category="Smartphone")  # Фільтруємо товари категорії Smartphone
    return render(request, 'main/smartphones.html', {"smartphones": smartphones})


# Представлення для ноутбуків
def LaptopsView(request):
    laptops = TechList.objects.filter(category="Laptop")  # Фільтруємо товари категорії Laptop
    return render(request, 'main/laptops.html', {"laptops": laptops})


# Представлення для мишок
def MousesView(request):
    mouses = TechList.objects.filter(category="Mouse")  # Фільтруємо товари категорії Mouse
    return render(request, 'main/mouses.html', {"mouses": mouses})


# Представлення для телевізорів
def TelevisionsView(request):
    televisions = TechList.objects.filter(category="Television")  # Фільтруємо товари категорії Television
    return render(request, 'main/televisions.html', {"televisions": televisions})


# Представлення для реєстрації користувача
def RegistrationView(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Зберігаємо дані в модель PendingUser до підтвердження email
            pending_user = PendingUser(
                email=form.cleaned_data['email'],
                full_name=form.cleaned_data['full_name'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data.get('address', ''),
                password=make_password(form.cleaned_data['password1']),
            )
            pending_user.save()

            # Формуємо посилання для підтвердження
            token = str(pending_user.token)  # Перетворюємо UUID у рядок для URL
            confirm_url = request.build_absolute_uri(reverse('main:confirm_email', args=[token]))

            # Надсилаємо email для підтвердження
            subject = 'Confirm Your Registration at DeviceMarket'
            message = f'Hello, {pending_user.full_name}!\n\nThank you for registering. Please click the link below to activate your account:\n{confirm_url}'
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [pending_user.email])

            # Повідомлення про успішну відправку листа
            messages.success(request, 'A confirmation email has been sent to your email address.')
            return redirect('main:login')  # Перенаправляємо на сторінку входу

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


# Представлення для підтвердження email
def ConfirmEmailView(request, token):
    try:
        # Шукаємо користувача в PendingUser за токеном
        pending_user = PendingUser.objects.get(token=token)

        # Створюємо нового користувача в таблиці User
        user = User.objects.create(
            email=pending_user.email,
            full_name=pending_user.full_name,
            phone=pending_user.phone,
            address=pending_user.address,
            password=pending_user.password,
            is_active=True  # Активуємо користувача
        )
        user.save()

        # Видаляємо запис із PendingUser
        pending_user.delete()

        # Додаємо повідомлення про успішне підтвердження
        messages.success(request, 'Account successfully confirmed! Please log in to continue.')
        return redirect('main:login')  # Перенаправляємо на сторінку входу
    except PendingUser.DoesNotExist:
        # Якщо токен не знайдено, показуємо помилку
        messages.error(request, 'Invalid or expired confirmation link.')
        return redirect('main:login')


# Представлення для входу (авторизації)
class LogInView(AuthLoginView):
    form_class = UserLoginForm
    template_name = 'main/login.html'


# Представлення для профілю користувача
def ProfileView(request):
    if not request.user.is_authenticated:
        return redirect('main:login')  # Якщо користувач не авторизований, перенаправляємо на сторінку входу
    return render(request, 'main/profile.html', {'user': request.user})

