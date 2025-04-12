from django.shortcuts import render
from rest_framework import viewsets
from ..models import Machinery
from ..serializers import MachinerySerializer
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from repairs.models import FaultCase
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes

# a viewset to view all machines at /api/machineries
# ReadOnlyModelViewSet provides list() and retrieve()
class MachineryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Machinery.objects.all().order_by('priority')
    serializer_class = MachinerySerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'name']  # enables ?status=[] and ?name=[]
    ordering_fields = ['priority', 'name']

# set permissions to check if manager
class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return getattr(user, 'role', '') == 'MANAGER'

# every request to /api/machineries/manage is accessed only by managers
# only managers can create, update or delete machines
class MachineryManagerViewSet(viewsets.ModelViewSet):
    queryset = Machinery.objects.all().order_by('priority') # viewed by priority
    serializer_class = MachinerySerializer
    permission_classes = [IsManager] # set permissions to manager
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'name'] # enables ?status=[] and ?name=[]
    ordering_fields = ['priority', 'name']

    # override create method for POST requests
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # custom response with message
        data = serializer.data
        data['message'] = "Machine was successfully created!"

        return Response(data, status=status.HTTP_201_CREATED)

    # override update method for PUT/PATCH requests
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False) # handles both PUT and PATCH requests

        # get the requested object ID from the URL
        pk = self.kwargs.get('pk')

        # checking if element exists
        if not Machinery.objects.filter(pk=pk).exists():
            # if the object doesn't exist, return a 404 response with a message
            return Response(
                {"error": f"Machine with id {pk} was not found."}, status=status.HTTP_404_NOT_FOUND
            )

        # if exists
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        # update
        self.perform_update(serializer)

        data = serializer.data
        # add custom message
        data['message'] = f"Machine '{instance.name}' was successfully updated!"
        return Response(data, status=status.HTTP_200_OK)

    # override destroy method for DELETE requests
    def destroy(self, request, *args, **kwargs):
        # get the requested object ID from the URL
        pk = self.kwargs.get('pk')

        if not Machinery.objects.filter(pk=pk).exists():
            # if the object doesn't exist, return a 404 response with a message
            return Response(
                {"error": f"Machine with id {pk} was not found."}, status=status.HTTP_404_NOT_FOUND
            )

        # if exists
        instance = self.get_object()
        machine_name = instance.name  # save the name before deletion
        self.perform_destroy(instance)

        # return custom message
        return Response({
            "message": f"Machine '{machine_name}' was successfully deleted!"}, status=status.HTTP_200_OK
        )

# get request to get the status of the machine
class MachineryStatusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Machinery.objects.all()
    serializer_class = MachinerySerializer

    def retrieve(self, request, pk=None):
        # checking if element exists
        if not Machinery.objects.filter(pk=pk).exists():
            return Response(
                {"error": f"Machine with id {pk} was not found."}, status=status.HTTP_404_NOT_FOUND
            )

        instance = self.queryset.get(pk=pk)

        # return just the status field
        return Response({'status': instance.status})

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def machinery_detail(request, machine_id):
    """API endpoint to get machinery details."""
    machinery = get_object_or_404(Machinery, machine_id=machine_id)
    
    # Only include fields that actually exist on the Machinery model
    machine_data = {
        'machine_id': machinery.machine_id,
        'name': machinery.name,
        'model': machinery.model,
        'description': machinery.description,
        'status': machinery.status,
        'priority': machinery.priority,
        'created_at': machinery.created_at.strftime('%Y-%m-%d') if hasattr(machinery, 'created_at') else None,
        'updated_at': machinery.updated_at.strftime('%Y-%m-%d') if hasattr(machinery, 'updated_at') else None,
        'last_maintained': machinery.last_maintained.strftime('%Y-%m-%d') if hasattr(machinery, 'last_maintained') and machinery.last_maintained else None,
    }
    
    return JsonResponse(machine_data)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def machinery_repairs(request, machine_id):
    """API endpoint to get repairs for a specific machine."""
    machine = get_object_or_404(Machinery, machine_id=machine_id)
    
    repairs = FaultCase.objects.filter(machine=machine)
    repairs_data = []
    
    for repair in repairs:
        # Get notes as a list if they exist
        notes = [note.note for note in repair.notes.all()] if hasattr(repair, 'notes') else []
        notes_text = "; ".join(notes) if notes else ""
        
        repairs_data.append({
            'id': repair.case_id,
            'status': repair.get_status_display(),
            'details': repair.description,
            'reported_by': repair.created_by.get_full_name() if repair.created_by else 'Unknown',
            'reported_date': repair.created_at.strftime('%Y-%m-%d'),
            'resolved_date': repair.resolved_at.strftime('%Y-%m-%d') if repair.resolved_at else None,
            'resolution_notes': repair.resolution_notes,
            'notes': notes_text,
            'priority': repair.priority
        })
    
    return JsonResponse(repairs_data, safe=False)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def machinery_counts(request):
    """API endpoint to get real-time counts of machinery by status."""
    ok_count = Machinery.objects.filter(status='OK').count()
    warning_count = Machinery.objects.filter(status='WARNING').count()
    fault_count = Machinery.objects.filter(status='FAULT').count()
    total_count = Machinery.objects.count()
    
    counts_data = {
        'ok_count': ok_count,
        'warning_count': warning_count,
        'fault_count': fault_count,
        'total_count': total_count
    }
    
    return JsonResponse(counts_data)
    