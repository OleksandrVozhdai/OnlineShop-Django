from django.urls import path
from .views import *

app_name = 'main'

urlpatterns = [
    path("", IndexView, name="index"),
    path("shop/", ShopView, name="shop"),
    path("about/", AboutView, name="about"),
    path("catalog/", CatalogView, name="catalog"),
    path("registration/", RegistrationView, name="registration"),
    path("login/", LogInView.as_view(), name="login"),
    path("activate/<int:user_id>/", ActivateView, name="activate"),
    path("shop/smartphones/", SmartphonesView, name="smartphones"),
    path("shop/laptops/", LaptopsView, name="laptops"),
    path("shop/mouses/", MousesView, name="mouses"),
    path("shop/televisions/", TelevisionsView, name="televisions"),
]