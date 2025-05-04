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
    path("shop/smartphones/", SmartphonesView, name="smartphones"),
    path("shop/laptops/", LaptopsView, name="laptops"),
    path("shop/mouses/", MousesView, name="mouses"),
    path("shop/televisions/", TelevisionsView, name="televisions"),
    path("shop/productPage/<int:id>/", ProductPageView, name="productPage"),

    path('toggle_wishlist/<int:id>/', Toggle_wishlist, name='toggle_wishlist'),
    path('add_to_cart/<int:product_id>/', AddToCartView, name='add_to_cart'),
    path("cart/", CartView, name="cart"),
    path('remove_from_cart/<int:product_id>/', RemoveFromCartView, name='remove_from_cart'),
    path('cart_item_count/', CartItemCountView, name='cart_item_count'),
path('add_to_cart/<int:tech_id>/', views.add_to_cart, name='add_to_cart'),
path('create_order/', views.create_order, name='create_order'),

]