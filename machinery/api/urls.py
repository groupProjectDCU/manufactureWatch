from django.urls import path
from .views import (
    MachineryViewSet, 
    MachineryManagerViewSet,
    MachineryStatusViewSet,
    machinery_detail,
    machinery_repairs,
    machinery_counts
)

urlpatterns = [
    # Original endpoints
    # /api/machinery/
    path('', MachineryViewSet.as_view({'get': 'list'}), name='machinery-list'),
    
    # /api/machinery/:id
    path('<int:pk>/', MachineryViewSet.as_view({'get': 'retrieve'}), name='machinery-detail'),
    
    # /api/machinery/:id/status
    path('<int:pk>/status/', MachineryStatusViewSet.as_view({'get': 'retrieve'}), name='machinery-status'),
    
    # /api/machinery/manage
    path('manage/', MachineryManagerViewSet.as_view({
        'get': 'list',  # GET request -> calls MachineryManagerViewSet.list() to show all machines
        'post': 'create'  # POST request -> calls MachineryManagerViewSet.create() to make a new machine
    }), name='machinery-manage-list'),
    
    # /api/machinery/manage/:id
    path('manage/<int:pk>/', MachineryManagerViewSet.as_view({
        'get': 'retrieve',  # GET request -> calls MachineryManagerViewSet.retrieve() to get one machine
        'put': 'update',  # PUT request -> calls MachineryManagerViewSet.update() for full update
        'patch': 'partial_update',  # PATCH request -> calls MachineryManagerViewSet.partial_update()
        'delete': 'destroy'  # DELETE request -> calls MachineryManagerViewSet.destroy() to delete a machine
    }), name='machinery-manage-detail'),
    
    # New endpoints for machine details and repair history - with correct path
    path('<int:machine_id>/details/', machinery_detail, name='machinery_detail'),
    path('<int:machine_id>/repairs/', machinery_repairs, name='machinery_repairs'),
    
    # Endpoint for real-time machinery counts
    path('counts/', machinery_counts, name='machinery_counts'),
] 