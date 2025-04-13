from django.urls import path
from . import views # Import the views from the current module

app_name = "repairs"

"""
All routes for fault case tracking are defined here.
    - User-facing:
        - GET /repairs/faults/                             -> View all fault cases
        - GET /repairs/faults/<uuid:fault_case_id>/        -> View a specific fault case
        - GET /repairs/faults/create/                      -> Create a new fault case (technician only)
        - GET /repairs/faults/<uuid:fault_case_id>/update/ -> Update a fault case
        - GET /repairs/faults/<uuid:fault_case_id>/fault_note_create/ -> Add a note to a specific fault case
"""
urlpatterns = [
    # User-facing URLs
    path('faults/', views.fault_case_list, name='fault_case_list'),
    path('faults/<uuid:fault_case_id>/', views.fault_case_detail, name='fault_case_detail'),
    path('faults/create/', views.fault_case_create, name='fault_case_create'),
    path('faults/<uuid:fault_case_id>/update/', views.fault_case_update, name='fault_case_update'),
    path('faults/<uuid:fault_case_id>/fault_note_create/', views.fault_note_create, name='fault_note_create')
]
