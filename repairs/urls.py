from django.urls import path
from . import views # Import the views from the current module

# Define URL patterns for the repairs app
# These patterns map URL paths to the corresponding view functions
urlpatterns = [
    # URL pattern for the fault case list view
    # Example: /faults/
    path('faults/', views.fault_case_list, name='fault_case_list'),

    # URL pattern for the fault case detail view, with a UUID 
    # Example: /faults/<uuid:fault_case_id>/
    path('faults/<uuid:fault_case_id>/', views.fault_case_detail, name='fault_case_detail'),

    # URL pattern for the fault case creation view
    # Example: /faults/create/
    path('faults/create/', views.fault_case_create, name='fault_case_create'),

    # URL for updating an existing fault case, with a UUID
    # Example: /faults/<uuid:fault_case_id>/update/
    path('faults/<uuid:fault_case_id>/update/', views.fault_case_update, name='fault_case_update'),

    # URL for creating a new fault note for a specific fault case, with a UUID
    # Example: /faults/<uuid:fault_case_id>/fault_note_create/
    path('faults/<uuid:fault_case_id>/fault_note_create/', views.fault_note_create, name='fault_note_create'),
]