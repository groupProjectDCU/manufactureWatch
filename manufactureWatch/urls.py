"""
URL configuration for manufactureWatch project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from accounts.urls import api_urlpatterns as accounts_api_urlpatterns
from machinery.urls import api_urlpatterns as machinery_api_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    # API Routes
    path('api/accounts/', include(accounts_api_urlpatterns)),
    path('api/machinery/', include(machinery_api_urlpatterns)),
    # Web Routes
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('repairs/', include('repairs.urls', namespace='repairs')),
]

