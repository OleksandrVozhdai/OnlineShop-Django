from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from main.models import TechList, Order

User = get_user_model()

class ModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            full_name='Test User',
            password='testpass123',
            phone='1234567890',
            address='123 Test St'
        )
        self.product = TechList.objects.create(
            product_name='Test Product',
            category='Electronics',
            brand='TestBrand',
            price=Decimal('199.99'),
            description='This is a test product',
            stock_quantity=10,
            author=self.user,
            stars=Decimal('4.5')
        )

    def test_techlist_creation(self):
        self.assertEqual(self.product.product_name, 'Test Product')
        self.assertEqual(self.product.category, 'Electronics')
        self.assertEqual(self.product.price, Decimal('199.99'))
        self.assertEqual(self.product.author, self.user)
        self.assertEqual(str(self.product), 'Test Product')

    def test_user_creation(self):
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertEqual(self.user.full_name, 'Test User')
        self.assertTrue(self.user.check_password('testpass123'))

    def test_order_creation(self):
        order = Order.objects.create(
            user=self.user,
            product=self.product,
            quantity=2,
            total_price=Decimal('399.98')
        )
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.product, self.product)
        self.assertEqual(order.quantity, 2)
        self.assertEqual(order.total_price, Decimal('399.98'))
        self.assertEqual(str(order), f"Order {order.id} by {self.user}")