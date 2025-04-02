from django.urls import path
from . import views


urlpatterns = [
    path('faults/', views.fault_case_list, name='fault_case_list'),
    path('faults/<uuid:fault_case_id>/', views.fault_case_detail, name='fault_case_detail'),
    path('faults/create/', views.fault_case_create, name='fault_case_create'),
    path('faults/<uuid:fault_case_id>/update/', views.fault_case_update, name='fault_case_update'),
    path('faults/<uuid:fault_case_id>/fault_note_create/', views.fault_note_create, name='fault_note_create'),
]