from django.shortcuts import render
from rest_framework import viewsets
from .models import Machinery
from .serializers import MachinerySerializer
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

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
