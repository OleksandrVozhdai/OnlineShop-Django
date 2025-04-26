from django.db import models
from django.contrib.auth.models import AbstractUser

# Кастомна модель користувача
class User(AbstractUser):
    id = models.AutoField(primary_key=True, db_column='UserID')
    full_name = models.CharField(max_length=255, db_column='FullName')
    email = models.EmailField(unique=True, db_column='Email')
    phone = models.CharField(max_length=20, blank=True, null=True, db_column='Phone')
    address = models.TextField(blank=True, null=True, db_column='Address')
    registration_date = models.DateTimeField(auto_now_add=True, db_column='RegistrationDate')

    # Поле для логіну (замість username використовуємо email)
    USERNAME_FIELD = 'email'

    # Обов'язкові поля при створенні користувача (наприклад, через createsuperuser)
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'Users'

# Модель для списку техніки
class TechList(models.Model):
    id = models.AutoField(primary_key=True, db_column='TechID')
    name = models.CharField(max_length=255, db_column='TechName', null=True)  # Додаємо null=True тимчасово
    category = models.CharField(max_length=255, db_column='Category')
    brand = models.CharField(max_length=255, db_column='Brand')
    price = models.DecimalField(max_digits=10, decimal_places=2, db_column='Price')
    image = models.ImageField(upload_to='tech_images/', blank=True, null=True, db_column='Image')

    def __str__(self):
        return self.name or "Unnamed Product"

    class Meta:
        db_table = 'TechList'

# Модель для замовлення
class Order(models.Model):
    id = models.AutoField(primary_key=True, db_column='OrderID')
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='UserID')
    tech = models.ForeignKey(TechList, on_delete=models.CASCADE, db_column='TechID', null=True)  # Додаємо null=True тимчасово
    order_date = models.DateTimeField(auto_now_add=True, db_column='OrderDate')
    quantity = models.IntegerField(db_column='Quantity')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, db_column='TotalPrice')

    def __str__(self):
        return f"Order {self.id} by {self.user}"

    class Meta:
        db_table = 'Orders'