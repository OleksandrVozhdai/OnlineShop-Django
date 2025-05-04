from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.http import JsonResponse
from decimal import Decimal
import random
from .forms import UserRegistrationForm, UserLoginForm, TechListForm
from .models import TechList, User, PendingUser

from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth import login
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserRegistrationForm, UserLoginForm
from .models import TechList, User
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Order, TechList
from django.utils import timezone
from django.contrib.auth.models import User
import string

# Представлення для головної сторінки
def IndexView(request):
    return render(request, 'main/index.html')

# Представлення для сторінки товару
def ProductPageView(request, id):
    product = get_object_or_404(TechList, id=id)
    all_products = TechList.objects.all()
    constAllProducts = random.sample(list(all_products), min(6, len(all_products)))

    relatedProducts = TechList.objects.filter(category=product.category).exclude(id=product.id)
    sameBrandProducts = TechList.objects.filter(brand=product.brand).exclude(id=product.id)[:6]
    sameUserProducts = TechList.objects.filter(author__username=product.author.username).exclude(id=product.id)

    return render(request, 'main/productPage.html', {
        'product': product,
        'relatedProducts': relatedProducts,
        'sameBrandProducts': sameBrandProducts,
        'constAllProducts': constAllProducts,
        'sameUserProducts': sameUserProducts
    })

# Перемикання стану "у списку бажань"
def Toggle_wishlist(request, id):
    if request.method == 'POST':
        product = get_object_or_404(TechList, id=id)
        product.on_wishlist = not product.on_wishlist
        product.save()
        return JsonResponse({'success': True, 'on_wishlist': product.on_wishlist})
    return JsonResponse({'success': False})

# Представлення для списку бажань
def WishlistView(request, id):
    product = get_object_or_404(TechList, id=id)
    all_products = TechList.objects.all()
    constAllProducts = random.sample(list(all_products), min(6, len(all_products)))
    wishlistProducts = TechList.objects.filter(on_wishlist=True)
    return render(request, 'main/wishlist.html', {
        'wishlistProducts': wishlistProducts,
        'product': product,
        'constAllProducts': constAllProducts,
    })

# Представлення для магазину з фільтрацією товарів
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

    rating = request.GET.get('rating')
    if rating:
        products = products.filter(stars__gte=Decimal(rating))

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

# Представлення для сторінки "Про нас"
def AboutView(request):
    return render(request, 'main/about.html')

# Представлення для каталогу
def CatalogView(request):
    products = TechList.objects.all()
    return render(request, 'main/catalog.html', {'products': products})

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
            token = str(pending_user.token)
            confirm_url = request.build_absolute_uri(reverse('main:confirm_email', args=[token]))

            # Надсилаємо email для підтвердження
            subject = 'Confirm Your Registration at DeviceMarket'
            message = f'Hello, {pending_user.full_name}!\n\nThank you for registering. Please click the link below to activate your account:\n{confirm_url}'
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [pending_user.email])

            # Повідомлення про успішну відправку листа
            messages.success(request, 'A confirmation email has been sent to your email address.')
            return redirect('main:login')
    else:
        form = UserRegistrationForm()
    return render(request, 'main/registration.html', {'form': form})

# Активація акаунта
def ActivateView(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.is_active = True
        user.save()
        return redirect('main:login')
    except User.DoesNotExist:
        return render(request, 'main/error.html', {'message': 'User not found'})

# Представлення для входу (авторизації)
class LogInView(AuthLoginView):
    form_class = UserLoginForm
    template_name = 'main/login.html'

# Представлення для підтвердження email
def ConfirmEmailView(request, token):
    try:
        pending_user = PendingUser.objects.get(token=token)
        user = User.objects.create(
            email=pending_user.email,
            full_name=pending_user.full_name,
            phone=pending_user.phone,
            address=pending_user.address,
            password=pending_user.password,
            is_active=True
        )
        user.save()
        pending_user.delete()
        messages.success(request, 'Account successfully confirmed! Please log in to continue.')
        return redirect('main:login')
    except PendingUser.DoesNotExist:
        messages.error(request, 'Invalid or expired confirmation link.')
        return redirect('main:login')

# Представлення для профілю користувача
def ProfileView(request):
    if not request.user.is_authenticated:
        return redirect('main:login')
    user_products = TechList.objects.filter(author=request.user)
    return render(request, 'main/profile.html', {
        'user': request.user,
        'user_products': user_products,
    })

@login_required
def add_product(request):
    if request.method == 'POST':
        form = TechListForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.author = request.user
            product.save()
            messages.success(request, 'Product successfully added!')
            return redirect('main:profile')
        else:
            messages.error(request, 'Please check the entered data.')
    else:
        form = TechListForm()
    return render(request, 'main/add_product.html', {'form': form})

@login_required
def delete_product(request, id):
    product = get_object_or_404(TechList, id=id, author=request.user)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product successfully deleted!')
        return redirect('main:profile')
    return render(request, 'main/delete_confirmation.html', {'product': product})

@login_required
def edit_product(request, id):
    product = get_object_or_404(TechList, id=id, author=request.user)
    if request.method == 'POST':
        form = TechListForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product successfully updated!')
            return redirect('main:profile')
    else:
        form = TechListForm(instance=product)
    return render(request, 'main/edit_product.html', {'form': form})

def search_products(request):
    query = request.GET.get('query', '')
    products = []

    if query:
        products = TechList.objects.filter(
            product_name__icontains=query
        ).filter(
            brand__icontains=query
        )

    # Перетворюємо продукти в список словників для JSON відповіді
    products_data = [{
        'id': product.id,
        'product_name': product.product_name,
        'brand': product.brand
    } for product in products]

    return JsonResponse({'products': products_data})

def CartView(request):
    cart = request.session.get('cart', [])
    cart = [int(product_id) for product_id in cart]
    products = TechList.objects.filter(id__in=cart)
    return render(request, 'main/cart.html', {'products': products})

@require_POST
def AddToCartView(request, product_id):
    cart = request.session.get('cart', [])
    if str(product_id) not in cart:
        cart.append(str(product_id))
    request.session['cart'] = cart
    return JsonResponse({'success': True})

@require_POST
def RemoveFromCartView(request, product_id):
    cart = request.session.get('cart', [])
    if str(product_id) in cart:
        cart.remove(str(product_id))
    request.session['cart'] = cart
    return JsonResponse({'success': True})

@csrf_exempt
def CartItemCountView(request):
    cart = request.session.get('cart', [])
    return JsonResponse({'count': len(cart)})

@csrf_exempt
@login_required
def add_to_cart(request, tech_id):
    if request.method == 'POST':
        try:
            tech = TechList.objects.get(id=tech_id)
            quantity = 1

            total_price = tech.price * quantity

            Order.objects.create(
                user=request.user,
                product=tech,
                order_date=timezone.now(),
                quantity=quantity,
                total_price=total_price
            )

            return JsonResponse({'success': True, 'message': 'Order created'})
        except TechList.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Item not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@csrf_exempt
@require_POST
def create_order(request):
    cart = request.session.get('cart', [])
    if not cart:
        return JsonResponse({'success': False, 'error': 'Cart is empty.'})
    try:
        default_user = User.objects.get(id=1)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Default user does not exist.'})

    for product_id in cart:
        try:
            tech = TechList.objects.get(id=product_id)
            quantity = 1
            total_price = tech.price * quantity

            Order.objects.create(
                user=default_user,
                product=tech,
                order_date=timezone.now(),
                quantity=quantity,
                total_price=total_price
            )
        except TechList.DoesNotExist:
            continue

    @require_POST
    def clear_cart(request):
        request.session['cart'] = {}
        request.session.modified = True
        return JsonResponse({'success': True})

def update_username(request):
    if request.method == "POST":
        username = request.POST.get('username')
        if not username:
            # Generate random 6-character username if empty
            username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        try:
            user = request.user
            user.username = username
            user.save()
            messages.success(request, "Username updated successfully!")
        except Exception as e:
            messages.error(request, f"Error updating username: {e}")
        return redirect('main:profile')
    return render(request, 'main/profile.html')