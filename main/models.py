from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from decimal import Decimal

# Модель для списку техніки
class TechList(models.Model):
    id = models.AutoField(primary_key=True, db_column='ID')
    product_name = models.CharField(max_length=255, db_column='ProductName', default='Unnamed Product')
    category = models.CharField(max_length=100, blank=True, null=True, db_column='Category')
    brand = models.CharField(max_length=100, blank=True, null=True, db_column='Brand')
    price = models.DecimalField(max_digits=10, decimal_places=2, db_column='Price')
    description = models.TextField(blank=True, null=True, db_column='Description')
    stock_quantity = models.IntegerField(db_column='StockQuantity', default=0)
    image_url = models.URLField(max_length=500, blank=True, null=True, db_column='ImageURL')
    on_sale = models.BooleanField(default=False, db_column='OnSale')
    on_wishlist = models.BooleanField(default=False, db_column='OnWishlist')
    author = models.ForeignKey('User', on_delete=models.CASCADE, related_name='products', null=True, db_column='author_id')
    stars = models.DecimalField(max_digits=3, decimal_places=1, default=0.0, db_column='Rating')

    def __str__(self):
        return self.product_name

    class Meta:
        db_table = 'TechList'

    @property
    def discounted_price(self):
        return round(self.price * Decimal('0.75'), 2)

# Кастомна модель користувача
class User(AbstractUser):
    id = models.AutoField(primary_key=True, db_column='UserID')
    password = models.CharField(max_length=128, db_column='Password', null=True, blank=True)
    full_name = models.CharField(max_length=255, db_column='FullName')
    email = models.EmailField(unique=True, db_column='Email')
    phone = models.CharField(max_length=20, blank=True, null=True, db_column='Phone')
    address = models.TextField(blank=True, null=True, db_column='Address')
    registration_date = models.DateTimeField(auto_now_add=True, db_column='RegistrationDate')
    username = models.CharField(max_length=255, db_column='username')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'Users'

# Модель для замовлень
class Order(models.Model):
    id = models.AutoField(primary_key=True, db_column='OrderID')
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='UserID')
    product = models.ForeignKey(TechList, on_delete=models.CASCADE, null=True, blank=True, db_column='ProductID')
    order_date = models.DateTimeField(auto_now_add=True, db_column='OrderDate')
    quantity = models.IntegerField(db_column='Quantity')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, db_column='TotalPrice')

    def __str__(self):
        return f"Order {self.id} by {self.user}"

    class Meta:
        db_table = 'Orders'

# Модель для зберігання даних користувачів до підтвердження email
class PendingUser(models.Model):
    email = models.EmailField(unique=True, db_column='Email')
    full_name = models.CharField(max_length=255, db_column='FullName')
    phone = models.CharField(max_length=20, blank=True, null=True, db_column='Phone')
    address = models.TextField(blank=True, null=True, db_column='Address')
    password = models.CharField(max_length=128, db_column='Password', null=True, blank=True)
    token = models.CharField(max_length=36, default=uuid.uuid4, unique=True, db_column='Token')
    created_at = models.DateTimeField(auto_now_add=True, db_column='CreatedAt')

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'PendingUsers'