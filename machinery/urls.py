# machinery/urls.py
from django.urls import path
from .views import MachineryViewSet, MachineryManagerViewSet, MachineryStatusViewSet

# TODO: implement nested routes: api/collections/:collection_id/machineries/:id

app_name = 'machinery'

'''
All routes for machines defined here.
    - api:
        - GET /api/machineries/ - List all machines
        - GET /api.machineries/?name=[NAME] - Lists all machine names under a specific name
        - GET /api.machineries/?status=[STATUS] - Lists all machines names with a specific status
        
        - GET /api/machineries/<machine_id>/ - Detail for a specific machine
        - GET /api/machineries/<machine_id>/status/ - Status for a specific machine

        - GET /api/machineries/manage/ - For managers to list all machines
        - GET /api/machineries/manage/?status=[STATUS] - For managers to list all machines with a specific status
        - GET /api/machineries/manage/?name=[NAME] - For managers to list all machines with a specific status
        - POST /api/machineries/manage/ - For managers to create a new machine
        - PUT/PATCH /api/machineries/manage/<machine_id>/ - For managers to update a machine
        - DELETE /api/machineries/manage/<machine_id>/ - For managers to delete a machine
'''

urlpatterns = [
    # /api/machineries
    path('machineries/', MachineryViewSet.as_view({'get': 'list'}), name='machinery-list'),

    # /api/machineries/:id
    path('machineries/<int:pk>/', MachineryViewSet.as_view({'get': 'retrieve'}), name='machinery-detail'),

    # /api/machineries/:id/status
    path('machineries/<int:pk>/status/', MachineryStatusViewSet.as_view({'get': 'retrieve'}), name='machinery-status'),

    # /api/machineries/manage
    path('machineries/manage/', MachineryManagerViewSet.as_view({
        'get': 'list', # GET request -> calls MachineryManagerViewSet.list() to show all machines
        'post': 'create' # POST request -> calls MachineryManagerViewSet.create() to make a new machine
    }), name='machinery-manage-list'),

    # /api/machineries/manage
    path('machineries/manage/<int:pk>/', MachineryManagerViewSet.as_view({
        'get': 'retrieve',  # GET request -> calls MachineryManagerViewSet.retrieve() to get one machine
        'put': 'update', # PUT request -> calls MachineryManagerViewSet.update() for full update
        'patch': 'partial_update', # PATCH request -> calls MachineryManagerViewSet.partial_update()
        'delete': 'destroy' # DELETE request -> calls MachineryManagerViewSet.destroy() to delete a machine
    }), name='machinery-manage-detail'),
]
