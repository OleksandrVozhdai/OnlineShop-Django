from django.test import TestCase
from main.forms import UserRegistrationForm, UserLoginForm, TechListForm

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