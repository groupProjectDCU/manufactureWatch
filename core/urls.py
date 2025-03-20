from django.urls import path
from . import views

urlpatterns = [
    path('home.html', views.home, name='home'),
    path('about.html', views.about, name='about'),
    path('contact.html', views.contact, name='contact'),
    path('login.html', views.login, name='login'),
    path('register.html', views.register, name='register'),
    path('forgotpass.html', views.forgotpass, name='forgotpass'),
]