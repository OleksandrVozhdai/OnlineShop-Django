from django.db import models

# Create your models here.

from django.db import models

class TechList(models.Model):
    id = models.AutoField(primary_key=True, db_column='ID')
    product_name = models.CharField(max_length=255, db_column='ProductName')
    category = models.CharField(max_length=100, blank=True, null=True, db_column='Category')
    brand = models.CharField(max_length=100, blank=True, null=True, db_column='Brand')
    price = models.DecimalField(max_digits=10, decimal_places=2, db_column='Price')
    description = models.TextField(blank=True, null=True, db_column='Description')
    stock_quantity = models.IntegerField(db_column='StockQuantity')
    image_url = models.URLField(max_length=500, blank=True, null=True, db_column='ImageURL')
    on_sale = models.BooleanField(default=False, db_column='OnSale')

    def __str__(self):
        return self.product_name

    class Meta:
        db_table = 'TechList'


class User(models.Model):
    id = models.AutoField(primary_key=True, db_column='UserID')
    full_name = models.CharField(max_length=255, db_column='FullName')
    email = models.EmailField(unique=True, db_column='Email')
    phone = models.CharField(max_length=20, blank=True, null=True, db_column='Phone')
    address = models.TextField(blank=True, null=True, db_column='Address')
    registration_date = models.DateTimeField(auto_now_add=True, db_column='RegistrationDate')

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'Users'


class Order(models.Model):
    id = models.AutoField(primary_key=True, db_column='OrderID')
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='UserID')
    product = models.ForeignKey(TechList, on_delete=models.CASCADE, db_column='ProductID')
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