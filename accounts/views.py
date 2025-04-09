from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from .serializers import UserSerializer
from .models import User
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny


@api_view(['POST'])
@csrf_exempt  # ❗ Only for API calls, not recommended for security reasons
@permission_classes([AllowAny])
def signup_view(request):
    """Handles user registration using session authentication"""
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        login(request, user)  # ✅ Logs in the user using session auth
        return JsonResponse({"message": "Signup successful", "user": serializer.data}, status=status.HTTP_201_CREATED)
    
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@csrf_exempt  # ❗ Only for API calls, not recommended for security reasons
@permission_classes([AllowAny])
def login_view(request):
    """Handles user login using session authentication"""
    data = json.loads(request.body)
    username = data.get("username")
    password = data.get("password")
    
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)  # ✅ Use Django’s session authentication
        return JsonResponse({"message": "Login successful", "user": UserSerializer(user).data}, status=status.HTTP_200_OK)

    return JsonResponse({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


 