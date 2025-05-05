from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('captcha/', views.captcha_image, name='captcha'),
]