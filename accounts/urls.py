from django.urls import path
from .views import signup_view, login_view 
 
app_name = 'accounts'

urlpatterns = [
    path('signup/', signup_view, name='signup'),  # User Registration
    path('login/', login_view, name='login')  # Login & Token Generation
    
]
