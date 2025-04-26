from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

# Форма для реєстрації
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Електронна пошта")
    full_name = forms.CharField(required=True, label="Повне ім'я")
    phone = forms.CharField(required=False, label="Телефон")
    address = forms.CharField(required=False, label="Адреса")

    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone', 'address', 'password1', 'password2']

# Форма для входу
class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Електронна пошта")  # username тут буде email
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)