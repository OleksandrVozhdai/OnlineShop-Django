from django.urls import path
from .views import *
from . import views

app_name = 'main'

urlpatterns = [
    path("", IndexView, name="index"),
    path("shop/", ShopView, name="shop"),
    path("about/", AboutView, name="about"),
    path("catalog/", CatalogView, name="catalog"),
    path("registration/", RegistrationView, name="registration"),
    path("login/", LogInView.as_view(), name="login"),
    path("wishlist/", WishlistView, name="wishlist"),
    path("activate/<int:user_id>/", ActivateView, name="activate"),
    path("shop/productPage/<int:id>/", ProductPageView, name="productPage"),
    path('toggle_wishlist/<int:id>/', Toggle_wishlist, name='toggle_wishlist'),
    path('confirm-email/<str:token>/', views.ConfirmEmailView, name='confirm_email'),
    path('profile/', views.ProfileView, name='profile'),
]