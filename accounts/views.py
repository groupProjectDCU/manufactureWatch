from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from .serializers import UserSerializer
from .models import User
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


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
        login(request, user)  # ✅ Use Django's session authentication
        return JsonResponse({"message": "Login successful", "user": UserSerializer(user).data}, status=status.HTTP_200_OK)

    return JsonResponse({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

# Web views for traditional form-based authentication
def web_login(request):
    """Handles user login via web form"""
    # If user is already logged in, redirect to appropriate dashboard
    if request.user.is_authenticated:
        return redirect_to_dashboard(request.user)
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Log the user in
            login(request, user)
            messages.success(request, f"Welcome back, {user.get_full_name() or user.username}!")
            
            # Redirect to appropriate dashboard based on role
            return redirect_to_dashboard(user)
        else:
            # Authentication failed
            messages.error(request, "Invalid username or password")
    
    # GET request or failed authentication
    return render(request, 'accounts/login.html')

def web_logout(request):
    """Handles user logout"""
    # Clear any existing messages
    storage = messages.get_messages(request)
    for message in storage:
        # This consumes the messages
        pass
    storage.used = False
    
    # Logout the user
    logout(request)
    
    # Add the logout success message with auto_dismiss flag to ensure it's picked up
    messages.info(request, "You have been logged out successfully.")
    
    # Redirect to login page
    return redirect('accounts:web_login')

def redirect_to_dashboard(user):
    """Redirect user to the appropriate dashboard based on their role"""
    user_role = user.role.upper() if user.role else ""
    
    if user_role == 'MANAGER':
        return redirect('accounts:manager_dashboard')
    elif user_role == 'TECHNICIAN':
        return redirect('accounts:technician_dashboard')
    elif user_role == 'REPAIR':
        return redirect('accounts:repair_dashboard')
    else:
        # Default dashboard for VIEW_ONLY or unknown roles
        return redirect('accounts:dashboard')

def web_register(request):
    """Handles user registration via web form"""
    if request.method == 'POST':
        # Get form data
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone_number = request.POST.get('phone', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        role = request.POST.get('role', '').upper()
        
        # Validate form data
        errors = []
        
        if not first_name or not last_name:
            errors.append("First name and last name are required.")
        
        if not email:
            errors.append("Email is required.")
        elif User.objects.filter(email=email).exists():
            errors.append("Email is already in use.")
            
        if not password:
            errors.append("Password is required.")
        elif password != confirm_password:
            errors.append("Passwords do not match.")
        elif len(password) < 8:
            errors.append("Password must be at least 8 characters long.")
            
        if not role:
            errors.append("Role selection is required.")
        elif role not in [choice[0] for choice in User.ROLE_CHOICES]:
            errors.append("Invalid role selected.")
        
        # If there are errors, show them to the user
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'accounts/register.html')
        
        # Create username from email
        username = email.split('@')[0]
        base_username = username
        counter = 1
        
        # Ensure username is unique
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        
        try:
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role=role
            )
            
            # Set phone number if the model has this field
            if hasattr(user, 'phone_number'):
                user.phone_number = phone_number
                user.save()
            
            # Log the user in
            login(request, user)
            
            # Success message
            messages.success(request, f"Welcome, {user.get_full_name() or user.username}! Your account has been created successfully.")
            
            # Redirect to appropriate dashboard
            return redirect_to_dashboard(user)
            
        except Exception as e:
            # Handle any errors during user creation
            messages.error(request, f"Error creating account: {str(e)}")
            return render(request, 'accounts/register.html')
    
    # GET request - show the registration form
    return render(request, 'accounts/register.html')

def web_forgotpass(request):
    """Handles password reset request"""
    return render(request, 'accounts/forgotpass.html')

@login_required
def update_profile(request):
    """Handle user profile updates via AJAX"""
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Get form data
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        current_password = request.POST.get('current_password', '')
        
        # Validate current password
        if not request.user.check_password(current_password):
            return JsonResponse({
                'success': False,
                'message': 'Current password is incorrect. Please try again.'
            })
        
        # Basic validation
        if not email:
            return JsonResponse({
                'success': False,
                'message': 'Email is required.'
            })
            
        # Check if email is already in use by another user
        if User.objects.exclude(pk=request.user.pk).filter(email=email).exists():
            return JsonResponse({
                'success': False,
                'message': 'Email is already in use by another account.'
            })
        
        # Update user profile
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        
        # Handle phone number
        # If User model has phone_number directly
        if hasattr(user, 'phone_number'):
            user.phone_number = phone_number
        # If User model has a UserProfile with phone_number
        elif hasattr(user, 'profile') and hasattr(user.profile, 'phone_number'):
            user.profile.phone_number = phone_number
            user.profile.save()
        # If we need to add phone_number as an extra field
        else:
            # Log the fact that we couldn't save the phone number
            print(f"Warning: Could not save phone number for user {user.username}. Field not found.")
            
        # Save the user after all changes
        user.save()
        
        # Get the saved phone number for response
        saved_phone = ''
        if hasattr(user, 'phone_number'):
            saved_phone = user.phone_number
        elif hasattr(user, 'profile') and hasattr(user.profile, 'phone_number'):
            saved_phone = user.profile.phone_number
            
        # Return success response with ALL updated user data
        return JsonResponse({
            'success': True,
            'message': 'Profile updated successfully.',
            'user': {
                'full_name': user.get_full_name(),
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'phone_number': saved_phone
            }
        })
    
    # Return error for non-AJAX or non-POST requests
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method.'
    }, status=400)

# Dashboard views (these should be added and connected to templates)
def dashboard(request):
    """Generic dashboard that redirects to login or appropriate role-specific dashboard"""
    # If user is not authenticated, redirect to login
    if not request.user.is_authenticated:
        messages.info(request, "Please log in to access your dashboard.")
        # Store the intended destination for after login
        return redirect('accounts:web_login')
    
    # For authenticated users, redirect to appropriate role-specific dashboard
    user_role = request.user.role.upper() if request.user.role else ""
    
    if user_role == 'MANAGER':
        return redirect('accounts:manager_dashboard')
    elif user_role == 'TECHNICIAN':
        return redirect('accounts:technician_dashboard')
    elif user_role == 'REPAIR':
        return redirect('accounts:repair_dashboard')
    else:
        # Only render the generic dashboard for VIEW_ONLY role
        return render(request, 'accounts/dashboard.html')

@login_required(login_url='accounts:web_login')
def manager_dashboard(request):
    """Dashboard for managers"""
    # Check if user has manager role
    if request.user.role != 'MANAGER':
        messages.error(request, "You don't have permission to access the manager dashboard.")
        return redirect('accounts:dashboard')
    return render(request, 'accounts/manager_dashboard.html')

@login_required(login_url='accounts:web_login')
def technician_dashboard(request):
    """Dashboard for technicians"""
    # Check if user has technician role
    if request.user.role != 'TECHNICIAN':
        messages.error(request, "You don't have permission to access the technician dashboard.")
        return redirect('accounts:dashboard')
    return render(request, 'accounts/technician_dashboard.html')

@login_required(login_url='accounts:web_login')
def repair_dashboard(request):
    """Dashboard for repair team"""
    # Check if user has repair role
    if request.user.role != 'REPAIR':
        messages.error(request, "You don't have permission to access the repair dashboard.")
        return redirect('accounts:dashboard')
    return render(request, 'accounts/repair_dashboard.html')

@login_required
def get_profile(request):
    """Return the user's profile data in JSON format for AJAX requests"""
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        user = request.user
        
        # Prepare user data
        user_data = {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'role': user.role,
            'role_display': user.get_role_display() if hasattr(user, 'get_role_display') else user.role,
            'phone_number': getattr(user, 'phone_number', '') if hasattr(user, 'phone_number') else '',
            'full_name': user.get_full_name()
        }
        
        return JsonResponse({
            'success': True,
            'user': user_data
        })
    
    # Return error for non-AJAX requests
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method.'
    }, status=400)

 