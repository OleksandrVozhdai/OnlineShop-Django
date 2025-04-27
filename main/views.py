from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView as AuthLoginView
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from .forms import UserRegistrationForm, UserLoginForm
from .models import TechList, User, PendingUser
from django.contrib.auth.hashers import make_password
from django.contrib import messages


# Представлення для головної сторінки
def IndexView(request):
    return render(request, 'main/index.html')


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

    # Отримуємо унікальні бренди та категорії для фільтрів
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