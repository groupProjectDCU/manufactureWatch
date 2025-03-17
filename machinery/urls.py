# In machinery/urls.py
from django.urls import path
from . import views

app_name = 'machinery'

urlpatterns = [
    path('', views.index, name='index'),  # This handles both /machinery and /machinery/

    # TODO: add paths to specific machines: /machinery/machine1
    # path('<int:machine_id>/', views.machine_detail, name='detail'),
    # path: /machinery/machine1/edit/
    # path('<int:machine_id>/edit/', views.edit_machine, name='edit'),
]