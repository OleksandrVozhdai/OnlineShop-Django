from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Кастомна модель користувача
class User(AbstractUser):
    id = models.AutoField(primary_key=True, db_column='UserID')  # Унікальний ідентифікатор користувача
    password = models.CharField(max_length=128, db_column='Password', null=True, blank=True)  # Дозволяємо null для поля password
    full_name = models.CharField(max_length=255, db_column='FullName')  # Повне ім'я користувача
    email = models.EmailField(unique=True, db_column='Email')  # Email користувача (унікальний)
    phone = models.CharField(max_length=20, blank=True, null=True, db_column='Phone')  # Телефон (опціонально)
    address = models.TextField(blank=True, null=True, db_column='Address')  # Адреса (опціонально)
    registration_date = models.DateTimeField(auto_now_add=True, db_column='RegistrationDate')  # Дата реєстрації

    # Поле для логіну (замість username використовуємо email)
    USERNAME_FIELD = 'email'

    # Обов'язкові поля при створенні користувача (наприклад, через createsuperuser)
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.full_name  # Повертаємо повне ім'я для зручного відображення

    class Meta:
        db_table = 'Users'  # Назва таблиці в базі даних

# Модель для списку техніки
class TechList(models.Model):
    id = models.AutoField(primary_key=True, db_column='TechID')  # Унікальний ідентифікатор товару
    name = models.CharField(max_length=255, db_column='TechName', null=True)  # Назва товару (тимчасово null=True)
    category = models.CharField(max_length=255, db_column='Category')  # Категорія товару
    brand = models.CharField(max_length=255, db_column='Brand')  # Бренд товару
    price = models.DecimalField(max_digits=10, decimal_places=2, db_column='Price')  # Ціна товару
    image = models.ImageField(upload_to='tech_images/', blank=True, null=True, db_column='Image')  # Зображення товару

    def __str__(self):
        return self.name or "Unnamed Product"  # Повертаємо назву товару або "Unnamed Product", якщо назва відсутня

    class Meta:
        db_table = 'TechList'  # Назва таблиці в базі даних

# Модель для замовлення
class Order(models.Model):
    id = models.AutoField(primary_key=True, db_column='OrderID')  # Унікальний ідентифікатор замовлення
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='UserID')  # Користувач, який зробив замовлення
    tech = models.ForeignKey(TechList, on_delete=models.CASCADE, db_column='TechID', null=True)  # Товар (тимчасово null=True)
    order_date = models.DateTimeField(auto_now_add=True, db_column='OrderDate')  # Дата замовлення
    quantity = models.IntegerField(db_column='Quantity')  # Кількість товару
    total_price = models.DecimalField(max_digits=10, decimal_places=2, db_column='TotalPrice')  # Загальна ціна

    def __str__(self):
        return f"Order {self.id} by {self.user}"  # Повертаємо опис замовлення

    class Meta:
        db_table = 'Orders'  # Назва таблиці в базі даних

# Модель для зберігання даних користувачів до підтвердження email
class PendingUser(models.Model):
    email = models.EmailField(unique=True, db_column='Email')  # Email користувача (унікальний)
    full_name = models.CharField(max_length=255, db_column='FullName')  # Повне ім'я
    phone = models.CharField(max_length=20, blank=True, null=True, db_column='Phone')  # Телефон (опціонально)
    address = models.TextField(blank=True, null=True, db_column='Address')  # Адреса (опціонально)
    password = models.CharField(max_length=128, db_column='Password', null=True, blank=True)  # Зашифрований пароль (дозволяємо null)
    token = models.CharField(max_length=36, default=uuid.uuid4, unique=True, db_column='Token')  # Змінено default
    created_at = models.DateTimeField(auto_now_add=True, db_column='CreatedAt')  # Дата створення запису

    def __str__(self):
        return self.email  # Повертаємо email для зручного відображення

    class Meta:
        db_table = 'PendingUsers'  # Назва таблиці в базі даних