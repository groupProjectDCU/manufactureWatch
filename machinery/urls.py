# machinery/urls.py
from django.urls import path
from .views import MachineryViewSet, MachineryManagerViewSet, MachineryStatusViewSet

# TODO: implement nested routes: api/collections/:collection_id/machineries/:id

app_name = 'machinery'

'''
All routes for machines defined here.
    - api:
        - GET /api/machinery/ - List all machines
        - GET /api/machinery/?name=[NAME] - Lists all machine names under a specific name
        - GET /api/machinery/?status=[STATUS] - Lists all machines names with a specific status
        
        - GET /api/machinery/<machine_id>/ - Detail for a specific machine
        - GET /api/machinery/<machine_id>/status/ - Status for a specific machine

        - GET /api/machinery/manage/ - For managers to list all machines
        - GET /api/machinery/manage/?status=[STATUS] - For managers to list all machines with a specific status
        - GET /api/machinery/manage/?name=[NAME] - For managers to list all machines with a specific status
        - POST /api/machinery/manage/ - For managers to create a new machine
        - PUT/PATCH /api/machinery/manage/<machine_id>/ - For managers to update a machine
        - DELETE /api/machinery/manage/<machine_id>/ - For managers to delete a machine
'''

# API endpoints
api_urlpatterns = ([
    # /api/machinery/
    path('', MachineryViewSet.as_view({'get': 'list'}), name='machinery-list'),

    # /api/machinery/:id
    path('<int:pk>/', MachineryViewSet.as_view({'get': 'retrieve'}), name='machinery-detail'),

    # /api/machinery/:id/status
    path('<int:pk>/status/', MachineryStatusViewSet.as_view({'get': 'retrieve'}), name='machinery-status'),

    # /api/machinery/manage
    path('manage/', MachineryManagerViewSet.as_view({
        'get': 'list', # GET request -> calls MachineryManagerViewSet.list() to show all machines
        'post': 'create' # POST request -> calls MachineryManagerViewSet.create() to make a new machine
    }), name='machinery-manage-list'),

    # /api/machinery/manage
    path('manage/<int:pk>/', MachineryManagerViewSet.as_view({
        'get': 'retrieve',  # GET request -> calls MachineryManagerViewSet.retrieve() to get one machine
        'put': 'update', # PUT request -> calls MachineryManagerViewSet.update() for full update
        'patch': 'partial_update', # PATCH request -> calls MachineryManagerViewSet.partial_update()
        'delete': 'destroy' # DELETE request -> calls MachineryManagerViewSet.destroy() to delete a machine
    }), name='machinery-manage-detail'),
], 'machinery_api')

# Web URLs (currently empty as this app only has API routes)
urlpatterns = []
