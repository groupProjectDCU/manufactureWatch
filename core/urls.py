from django.urls import path
from . import views

urlpatterns = [
    # Static Pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('userguide/', views.userguide, name='userguide'),
]