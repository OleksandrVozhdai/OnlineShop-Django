from django.contrib.auth.views import LoginView
from django.urls import path
from twisted.protocols.sip import Registration

from main.views import *

app_name = 'main'

urlpatterns = [
    path("", IndexView),
    path("shop/", ShopView, name="shop"),
    path("about/", AboutView, name="about"),
    path("catalog/", CatalogView, name="catalog"),
    path("registration/", RegistrationView, name="registration"),
    path("login/", LogInView, name="login"),
]