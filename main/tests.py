from django.test import TestCase
from main.models import TechList, User, Order, PendingUser
from decimal import Decimal


class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            email="user@example.com",
            full_name="Test User",
            password="password123",
            username="testuser"
        )
        self.assertEqual(user.email, "user@example.com")
        self.assertEqual(user.full_name, "Test User")


class TechListModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="owner@example.com",
            full_name="Owner",
            password="password123",
            username="owner"
        )

    def test_create_product(self):
        product = TechList.objects.create(
            product_name="Laptop",
            category="Computers",
            brand="Dell",
            price=Decimal('1000.00'),
            stock_quantity=10,
            on_sale=True,
            author=self.user,
            stars=4.5
        )
        self.assertEqual(product.product_name, "Laptop")
        self.assertEqual(product.discounted_price, Decimal('750.00'))
        self.assertTrue(product.on_sale)
        self.assertEqual(product.author, self.user)


class PendingUserModelTest(TestCase):
    def test_create_pending_user(self):
        pending = PendingUser.objects.create(
            email="pending@example.com",
            full_name="Pending User",
            phone="123456789",
            address="Test address",
            password="somepass"
        )
        self.assertEqual(pending.email, "pending@example.com")
        self.assertTrue(pending.token)
        self.assertIsNotNone(pending.created_at)
