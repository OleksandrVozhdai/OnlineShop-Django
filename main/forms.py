from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

# Форма для реєстрації
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")
    full_name = forms.CharField(required=True, label="Full name")
    phone = forms.CharField(required=False, label="Phone number")
    address = forms.CharField(required=False, label="Adress")

    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone', 'address', 'password1', 'password2']

# Форма для входу
class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")  # username тут буде email
    password = forms.CharField(label="Password", widget=forms.PasswordInput)