from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

app_name = 'main'

urlpatterns = [
    path("", IndexView, name="index"),
    path("shop/", ShopView, name="shop"),
    path("about/", AboutView, name="about"),
    path("catalog/", CatalogView, name="catalog"),
    path("registration/", RegistrationView, name="registration"),
    path("login/", LogInView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page='main:index'), name="logout"),
    path("wishlist/<int:id>/", WishlistView, name="wishlist"),
    path("activate/<int:user_id>/", ActivateView, name="activate"),
    path("shop/productPage/<int:id>/", ProductPageView, name="productPage"),
    path('toggle_wishlist/<int:id>/', Toggle_wishlist, name='toggle_wishlist'),
    path('confirm-email/<str:token>/', ConfirmEmailView, name='confirm_email'),
    path('profile/', ProfileView, name='profile'),
    path('add-product/', add_product, name='add_product'),
    path('delete-product/<int:product_id>/', delete_product, name='delete_product'),
    path('edit-product/<int:product_id>/', edit_product, name='edit_product'),
]