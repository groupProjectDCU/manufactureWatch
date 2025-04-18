from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

# Web URLs for traditional form-based authentication
urlpatterns = [
    # Authentication URLs
    path('login/', views.web_login, name='web_login'),
    path('logout/', views.web_logout, name='web_logout'),
    path('register/', views.web_register, name='web_register'),
    
    # Password recovery
    path('password-reset/', views.web_forgotpass, name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    # User profile management
    path('update-profile/', views.update_profile, name='update_profile'),
    path('get-profile/', views.get_profile, name='get_profile'),
    
    # Dashboard routes
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/manager/', views.manager_dashboard, name='manager_dashboard'),
    path('dashboard/technician/', views.technician_dashboard, name='technician_dashboard'),
    path('dashboard/repair/', views.repair_dashboard, name='repair_dashboard'),

    # Add from /dashboard
    path('dashboard/manager/machines/create', views.create_machines, name='create_machines'),
    path('dashboard/manager/machines/<int:machine_id>/edit/', views.update_machines, name='update_machines'),
    path('dashboard/manager/machines/<int:machine_id>/delete/', views.delete_machine, name='delete_machine'),
    path('dashboard/manager/machines/<int:machine_id>/export/', views.export_machine_by_id, name='export_machine_by_id'),
    path('dashboard/manager/collections/<int:collection_id>/export/', views.export_machines_by_collection, name='export_machines_by_collection'),

    path('dashboard/manager/collections/create/', views.create_collection, name='create_collection'),
    path('dashboard/manager/collections/<int:collection_id>/delete/', views.delete_collection, name='delete_collection'),
]
