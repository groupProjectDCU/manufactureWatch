from django.urls import path
from . import views

urlpatterns = [
    # /api/machinery/
    path('', views.MachineryViewSet.as_view({'get': 'list'}), name='machinery-list'),

    # /api/machinery/:id
    path('<int:pk>/', views.MachineryViewSet.as_view({'get': 'retrieve'}), name='machinery-detail'),

    # /api/machinery/:id/status
    path('<int:pk>/status/', views.MachineryStatusViewSet.as_view({'get': 'retrieve'}), name='machinery-status'),

    # /api/machinery/manage
    path('manage/', views.MachineryManagerViewSet.as_view({
        'get': 'list',  # GET request -> calls MachineryManagerViewSet.list() to show all machines
        'post': 'create'  # POST request -> calls MachineryManagerViewSet.create() to make a new machine
    }), name='machinery-manage-list'),

    # /api/machinery/manage/:id
    path('manage/<int:pk>/', views.MachineryManagerViewSet.as_view({
        'get': 'retrieve',  # GET request -> calls MachineryManagerViewSet.retrieve() to get one machine
        'put': 'update',  # PUT request -> calls MachineryManagerViewSet.update() for full update
        'patch': 'partial_update',  # PATCH request -> calls MachineryManagerViewSet.partial_update()
        'delete': 'destroy'  # DELETE request -> calls MachineryManagerViewSet.destroy() to delete a machine
    }), name='machinery-manage-detail'),
] 