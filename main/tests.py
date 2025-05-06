from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import mail
from decimal import Decimal
from main.forms import UserRegistrationForm, UserLoginForm, TechListForm
from main.models import TechList, Order, PendingUser

User = get_user_model()

class FormTests(TestCase):
    def test_user_registration_form(self):
        form_data = {
            'email': 'formuser@example.com',
            'full_name': 'Form User',
            'phone': '1234567890',
            'password1': 'formpass123',
            'password2': 'formpass123'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_login_form(self):
        User.objects.create_user(
            username='formuser',
            email='formuser@example.com',
            full_name='Form User',
            password='formpass123',
            phone='1234567890'
        )
        form_data = {
            'username': 'formuser@example.com',
            'password': 'formpass123'
        }
        form = UserLoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_techlist_form(self):
        form_data = {
            'product_name': 'Form Product',
            'category': 'Gadgets',
            'brand': 'FormBrand',
            'price': '399.99',
            'description': 'A form product',
            'stock_quantity': 20,
            'stars': '4.2'
        }
        form = TechListForm(data=form_data)
        self.assertTrue(form.is_valid())

class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
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
            product_id=self.product.id,
            quantity=2,
            total_price=Decimal('399.98')
        )
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.product_id, self.product.id)
        self.assertEqual(order.quantity, 2)
        self.assertEqual(order.total_price, Decimal('399.98'))
        self.assertEqual(str(order), f"Order {order.id} by {self.user}")

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            full_name='Test User',
            password='testpass123',
            phone='1234567890'
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

    def test_index_view(self):
        response = self.client.get(reverse('main:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/index.html')

    def test_shop_view(self):
        response = self.client.get(reverse('main:shop'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/shop.html')
        self.assertIn('products', response.context)

    def test_profile_view_unauthenticated(self):
        response = self.client.get(reverse('main:profile'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main:login'))

    def test_profile_view_authenticated(self):
        self.client.login(email='testuser@example.com', password='testpass123')
        response = self.client.get(reverse('main:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/profile.html')
        self.assertIn('user_products', response.context)

    def test_registration_view(self):
        response = self.client.get(reverse('main:registration'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/registration.html')

        data = {
            'email': 'newuser@example.com',
            'full_name': 'New User',
            'phone': '9876543210',
            'password1': 'newpass123',
            'password2': 'newpass123'
        }
        response = self.client.post(reverse('main:registration'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main:login'))
        self.assertTrue(PendingUser.objects.filter(email='newuser@example.com').exists())
        self.assertEqual(len(mail.outbox), 1)

    def test_login_view(self):
        response = self.client.get(reverse('main:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/login.html')

        response = self.client.post(reverse('main:login'), {
            'username': 'testuser@example.com',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_add_product(self):
        self.client.login(email='testuser@example.com', password='testpass123')
        response = self.client.get(reverse('main:add_product'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/add_product.html')

        data = {
            'product_name': 'New Product',
            'category': 'Gadgets',
            'brand': 'NewBrand',
            'price': '299.99',
            'description': 'A new product',
            'stock_quantity': 5,
            'stars': '4.0'
        }
        response = self.client.post(reverse('main:add_product'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main:profile'))
        self.assertTrue(TechList.objects.filter(product_name='New Product').exists())

    def test_edit_product(self):
        self.client.login(email='testuser@example.com', password='testpass123')
        response = self.client.get(reverse('main:edit_product', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/edit_product.html')

        data = {
            'product_name': 'Updated Product',
            'category': 'Electronics',
            'brand': 'TestBrand',
            'price': '249.99',
            'description': 'Updated description',
            'stock_quantity': 15,
            'stars': '4.8'
        }
        response = self.client.post(reverse('main:edit_product', args=[self.product.id]), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main:profile'))
        self.product.refresh_from_db()
        self.assertEqual(self.product.product_name, 'Updated Product')
        self.assertEqual(self.product.price, Decimal('249.99'))

    def test_delete_product(self):
        self.client.login(email='testuser@example.com', password='testpass123')
        response = self.client.get(reverse('main:delete_product', args=[self.product.id]))  # Исправлено
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/delete_confirmation.html')

        response = self.client.post(reverse('main:delete_product', args=[self.product.id]))  # Исправлено
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main:profile'))
        self.assertFalse(TechList.objects.filter(id=self.product.id).exists())

    def test_cart_functionality(self):
        response = self.client.post(reverse('main:add_to_cart', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True})

        response = self.client.get(reverse('main:cart_item_count'))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'count': 1})

        response = self.client.get(reverse('main:cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/cart.html')

        response = self.client.post(reverse('main:remove_from_cart', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True})

        response = self.client.get(reverse('main:cart_item_count'))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'count': 0})