from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.IndexView, name='index'),
    path('shop/', views.ShopView, name='shop'),
    path('about/', views.AboutView, name='about'),
    path('catalog/', views.CatalogView, name='catalog'),
    path('smartphones/', views.SmartphonesView, name='smartphones'),
    path('laptops/', views.LaptopsView, name='laptops'),
    path('mouses/', views.MousesView, name='mouses'),
    path('televisions/', views.TelevisionsView, name='televisions'),
    path('registration/', views.RegistrationView, name='registration'),
    path('confirm-email/<str:token>/', views.ConfirmEmailView, name='confirm_email'),
    path('login/', views.LogInView.as_view(), name='login'),
    path('profile/', views.ProfileView, name='profile'),
]