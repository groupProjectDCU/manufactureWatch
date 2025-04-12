from django.urls import path
from . import views

urlpatterns = [
    path('counts/', views.repair_counts, name='repair_counts'),
    path('', views.repairs_list, name='repairs_list'),
    path('<uuid:repair_id>/', views.repair_detail, name='repair_detail'),
    path('<uuid:repair_id>/complete/', views.repair_complete, name='repair_complete'),
    path('<uuid:repair_id>/start/', views.repair_start, name='repair_start'),
    path('<uuid:repair_id>/update/', views.repair_update, name='repair_update'),
] 