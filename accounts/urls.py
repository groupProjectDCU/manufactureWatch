from django.urls import path
from .views import signup_view, login_view, logout_view, protected_view
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'accounts'

urlpatterns = [
    path('signup/', signup_view, name='signup'),  # User Registration
    path('login/', login_view, name='login'),  # Login & Token Generation
    path('logout/', logout_view, name='logout'),  # Logout
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh Token
    path('protected/', protected_view, name='protected'),  # ✅ New Protected API
]
