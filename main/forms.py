from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from .models import TechList

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


from django import forms
from .models import TechList


class TechListForm(forms.ModelForm):
    class Meta:
        model = TechList
        fields = ['product_name', 'category', 'brand', 'price', 'description', 'stock_quantity', 'image_url', 'on_sale',
                  'on_wishlist']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product_name'].widget.attrs.update({'placeholder': 'Enter product name'})
        self.fields['category'].widget.attrs.update({'placeholder': 'Select category'})
        self.fields['brand'].widget.attrs.update({'placeholder': 'Enter brand'})
        self.fields['price'].widget.attrs.update({'placeholder': 'Enter price in USD'})
        self.fields['description'].widget.attrs.update({'placeholder': 'Enter product description'})
        self.fields['stock_quantity'].widget.attrs.update({'placeholder': 'Enter stock quantity'})
        self.fields['image_url'].widget.attrs.update({'placeholder': 'Enter image URL'})