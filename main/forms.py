from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

# Форма для реєстрації користувача
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")
    full_name = forms.CharField(max_length=255, required=True, label="Full Name")
    phone = forms.CharField(max_length=20, required=False, label="Phone")
    address = forms.CharField(required=False, label="Address")

    class Meta:
        model = User
        fields = ['email', 'full_name', 'phone', 'address', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

# Форма для входу (авторизації)
class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")  # Використовуємо email як ім'я користувача
    password = forms.CharField(widget=forms.PasswordInput, label="Password")