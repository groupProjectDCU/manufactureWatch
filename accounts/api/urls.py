from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='api_signup'),
    path('login/', views.login_view, name='api_login'),
] 