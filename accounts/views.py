import csv
from collections import defaultdict

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

from machinery.models import Machinery, MachineryAssignment, Collection, MachineryCollection
from .serializers import UserSerializer
from .models import User
from repairs.models import FaultCase
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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

    machines = Machinery.objects.all().prefetch_related('machinerycollection_set__collection')
    machine_collections = defaultdict(list)
    assignments = {}

    # Count machine statuses
    ok_count = machines.filter(status="OK").count()
    warning_count = machines.filter(status="WARNING").count()
    fault_count = machines.filter(status="FAULT").count()
    total_count = machines.count()

    for machine in machines:
        assignment = (
            MachineryAssignment.objects.filter(machine=machine, is_active=True)
            .select_related('assigned_to')
            .last()
        )
        assignments[machine.machine_id] = assignment

        # Get all collection names for this machine
        for mc in machine.machinerycollection_set.all():
            machine_collections[machine.machine_id].append(mc.collection.name)

    # Adding collections
    collections = Collection.objects.prefetch_related('machines').order_by('name')

    collection_summaries = []
    for collection in collections:
        # Get distinct only
        related_machines = collection.machines.all().distinct()

        collection_summaries.append({
            'id': collection.collection_id,
            'name': collection.name,
            'description': collection.description,
            'machines': related_machines
        })

    # Render
    return render(request, 'accounts/manager_dashboard.html', {
        'machines': machines,
        'assignments': assignments,
        'machine_collections': dict(machine_collections),
        'ok_count': ok_count,
        'warning_count': warning_count,
        'fault_count': fault_count,
        'total_count': total_count,
        'collection_summaries': collection_summaries
    })

@login_required(login_url='accounts:web_login')
def technician_dashboard(request):
    if request.user.role != 'TECHNICIAN':
        messages.error(request, "You don't have permission to access the technician dashboard.")
        return redirect('accounts:dashboard')

    # Fetch machines assigned to this technician
    assigned_ids = MachineryAssignment.objects.filter(
        assigned_to=request.user,
        is_active=True
    ).values_list('machine_id', flat=True)

    if assigned_ids:
        assigned_machines = Machinery.objects.filter(
            machine_id__in=assigned_ids
        ).prefetch_related('machinerycollection_set__collection')
        fallback_used = False
    else:
        # Fallback: show all machines
        assigned_machines = Machinery.objects.all().prefetch_related('machinerycollection_set__collection')
        fallback_used = True

    fault_cases = {}
    for machine in assigned_machines:
        fault = FaultCase.objects.filter(machine=machine).order_by('-created_at').first()
        if fault:
            fault_cases[machine.machine_id] = fault.case_id

    return render(request, 'accounts/technician_dashboard.html', {
        'assigned_machines': assigned_machines,
        'fallback_used': fallback_used,
        'fault_cases': fault_cases
    })

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

# Only managers are able to add machines
# accounts/dashboard/manager/machines/create
@login_required(login_url='accounts:web_login')
def create_machines(request):
    # Check if user has manager role
    if request.user.role != 'MANAGER':
        messages.error(request, "You don't have permission to access the manager dashboard.")
        return redirect('accounts:dashboard')

    staff = User.objects.filter(role__in=['TECHNICIAN', 'REPAIR'])
    collections = Collection.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        model = request.POST.get('model', '').strip()
        description = request.POST.get('description', '').strip()
        status = request.POST.get('status', '').strip()
        priority = request.POST.get('priority', '').strip()
        assigned_tech_id = request.POST.get('assigned_technician')
        assigned_repair_id = request.POST.get('assigned_repair')
        collection_ids = request.POST.getlist('collections')  # List of selected collection IDs

        # models.py say that machinery.model can be blank
        errors = []
        if not name:
            errors.append("Machine name is required.")
        if not description:
            errors.append("Machine description is required.")
        if not status:
            errors.append("Machine status is required.")
        if not priority:
            errors.append("Machine priority is required.")
        elif Machinery.objects.filter(model=model).exists():
            errors.append("A machine with this serial number already exists.")

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'accounts/create_machinery.html',
                          {'staff': staff, 'collections': collections})

        # Save the new machine
        machine = Machinery.objects.create(
            name=name,
            model=model,
            description=description,
            status=status,
            priority=int(priority)
        )

        # Assign the machine to a technician
        if assigned_tech_id:
            try:
                tech = User.objects.get(pk=assigned_tech_id, role='TECHNICIAN')
                MachineryAssignment.objects.create(
                    machine=machine,
                    assigned_by=request.user,
                    assigned_to=tech,
                    is_active=True
                )
            except User.DoesNotExist:
                messages.warning(request, "Technician not found.")

        # Assign machine to repairman
        if assigned_repair_id:
            try:
                repair = User.objects.get(pk=assigned_repair_id, role='REPAIR')
                MachineryAssignment.objects.create(
                    machine=machine,
                    assigned_by=request.user,
                    assigned_to=repair,
                    is_active=True
                )
            except User.DoesNotExist:
                messages.warning(request, "Repair person not found.")

        # Assign machine to selected collections
        for collection_id in collection_ids:
            if not collection_id.strip():
                continue
            try:
                collection = Collection.objects.get(pk=collection_id)
                MachineryCollection.objects.create(machinery=machine, collection=collection)
            except Collection.DoesNotExist:
                continue

        messages.success(request, f"Machine '{machine.name}' added successfully.")
        return redirect('accounts:manager_dashboard')

    # GET request
    return render(request, 'accounts/create_machinery.html',
                  {'staff': staff, 'collections': collections})

# Only managers are able to update machines
# accounts/dashboard/manager/machines/
@login_required(login_url='accounts:web_login')
def update_machines(request, machine_id):
    # Make sure only managers can access
    if request.user.role != 'MANAGER':
        messages.error(request, "You don't have permission to access this page.")
        return redirect('accounts:dashboard')

    # Get machine + all relevant staff + collections + assignments
    machine = get_object_or_404(Machinery, pk=machine_id)
    staff = User.objects.filter(role__in=['TECHNICIAN', 'REPAIR'])
    collections = Collection.objects.all()
    selected_collection_ids = machine.machinerycollection_set.values_list('collection_id', flat=True)
    all_assignments = MachineryAssignment.objects.select_related('machine', 'assigned_to', 'assigned_by').order_by('-assigned_at')

    if request.method == 'POST':
        # Pull form data
        name = request.POST.get('name', '').strip()
        model = request.POST.get('model', '').strip()
        description = request.POST.get('description', '').strip()
        status = request.POST.get('status', '').strip()
        priority = request.POST.get('priority', '').strip()
        assigned_tech_id = request.POST.get('assigned_technician')
        assigned_repair_id = request.POST.get('assigned_repair')
        collection_ids = request.POST.getlist('collections')

        # Validate input
        errors = []
        if not name:
            errors.append("Machine name is required.")
        if not description:
            errors.append("Machine description is required.")
        if not status:
            errors.append("Machine status is required.")
        if not priority:
            errors.append("Machine priority is required.")
        if model and Machinery.objects.exclude(pk=machine_id).filter(model=model).exists():
            errors.append("Another machine with this model already exists.")

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'accounts/update_machinery.html', {
                'machine': machine,
                'staff': staff,
                'collections': collections,
                'selected_collections': selected_collection_ids,
                'all_assignments': all_assignments
            })

        # Save changes
        machine.name = name
        machine.model = model
        machine.description = description
        machine.status = status
        machine.priority = int(priority)
        machine.save()

        # Handle assignment
        # Clear previous active assignments
        MachineryAssignment.objects.filter(machine=machine, is_active=True).update(is_active=False)

        # Assign technician
        if assigned_tech_id:
            try:
                tech = User.objects.get(pk=assigned_tech_id, role='TECHNICIAN')
                MachineryAssignment.objects.create(
                    machine=machine,
                    assigned_by=request.user,
                    assigned_to=tech,
                    is_active=True
                )
            except User.DoesNotExist:
                messages.warning(request, "Technician not found.")

        # Assign repair person
        if assigned_repair_id:
            try:
                repair = User.objects.get(pk=assigned_repair_id, role='REPAIR')
                MachineryAssignment.objects.create(
                    machine=machine,
                    assigned_by=request.user,
                    assigned_to=repair,
                    is_active=True
                )
            except User.DoesNotExist:
                messages.warning(request, "Repair person not found.")

        # Update collections
        MachineryCollection.objects.filter(machinery=machine).delete()
        for collection_id in collection_ids:
            if not collection_id.strip():
                continue
            try:
                collection = Collection.objects.get(pk=collection_id)
                MachineryCollection.objects.create(machinery=machine, collection=collection)
            except Collection.DoesNotExist:
                continue

        messages.success(request, f"Machine '{machine.name}' updated successfully.")
        return redirect('accounts:manager_dashboard')

    # GET request
    return render(request, 'accounts/update_machinery.html', {
        'machine': machine,
        'staff': staff,
        'collections': collections,
        'selected_collections': selected_collection_ids,
        'all_assignments': all_assignments
    })


# Only managers are able to delete machines
# accounts/dashboard/manager/machines/<int:machine_id>/delete/'
@login_required(login_url='accounts:web_login')
def delete_machine(request, machine_id):
    if request.user.role != 'MANAGER':
        messages.error(request, "You don't have permission to delete machines.")
        return redirect('accounts:dashboard')

    machine = get_object_or_404(Machinery, pk=machine_id)
    machine.delete()
    messages.success(request, f"Machine '{machine.name}' was deleted successfully.")
    return redirect('accounts:manager_dashboard')

# Managers can generate reports!
# Generate report for machines BY ID
@login_required(login_url='accounts:web_login')
def export_machine_by_id(request, machine_id):
    if request.user.role != 'MANAGER':
        messages.error(request, "You don't have permission to export this report.")
        return redirect('accounts:dashboard')

    # Get machine
    machine = get_object_or_404(Machinery, pk=machine_id)

    # Create the HttpResponse object with CSV headers
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="machine_{machine_id}_report.csv"'

    writer = csv.writer(response)
    # Rows
    writer.writerow(['ID', 'Name', 'Model', 'Status', 'Priority', 'Description', 'Assigned To', 'Assigned By', 'Collection(s)'])

    assignment = MachineryAssignment.objects.filter(machine=machine, is_active=True).select_related('assigned_to', 'assigned_by').last()
    assigned_to = assignment.assigned_to.get_full_name() if assignment and assignment.assigned_to else "Unassigned"
    assigned_by = assignment.assigned_by.get_full_name() if assignment and assignment.assigned_by else "Unknown"
    collections = ', '.join(c.collection.name for c in machine.machinerycollection_set.select_related('collection').all())

    # Write machine to CSV
    writer.writerow([
        machine.machine_id,
        machine.name,
        machine.model,
        machine.status,
        machine.priority,
        machine.description,
        assigned_to,
        assigned_by,
        collections
    ])

    return response

# Managers can generate reports!
# Generate report for machines BY COLLECTION_ID
@login_required(login_url='accounts:web_login')
def export_machines_by_collection(request, collection_id):
    if request.user.role != 'MANAGER':
        messages.error(request, "You don't have permission to export this report.")
        return redirect('accounts:dashboard')

    # Get machine
    collection = get_object_or_404(Collection, pk=collection_id)
    # Get machines that belong to this collection through the many-to-many relationship
    machines = (Machinery.objects
                .filter(machinerycollection__collection_id=collection_id)
                .prefetch_related('machinerycollection_set__collection'))

    # Create the HttpResponse object with CSV headers
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="collection_{collection.name}_report.csv"'

    writer = csv.writer(response)
    # Rows
    writer.writerow(['ID', 'Name', 'Model', 'Status', 'Priority', 'Description', 'Assigned To', 'Assigned By', 'Collection(s)'])

    for machine in machines:
        assignment = MachineryAssignment.objects.filter(machine=machine, is_active=True).select_related('assigned_to', 'assigned_by').last()
        assigned_to = assignment.assigned_to.get_full_name() if assignment and assignment.assigned_to else "Unassigned"
        assigned_by = assignment.assigned_by.get_full_name() if assignment and assignment.assigned_by else "Unknown"
        collections = ', '.join(c.collection.name for c in machine.machinerycollection_set.select_related('collection').all())

        # Write machines to CSV
        writer.writerow([
            machine.machine_id,
            machine.name,
            machine.model,
            machine.status,
            machine.priority,
            machine.description,
            assigned_to,
            assigned_by,
            collections
        ])

    return response

# If manager, create a collection
@login_required(login_url='accounts:web_login')
def create_collection(request):
    if request.user.role != 'MANAGER':
        messages.error(request, "You don't have permission to create collections.")
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()

        if not name:
            messages.error(request, "Collection name is required.")
            return render(request, 'accounts/create_collection.html')

        # Check for duplicates
        if Collection.objects.filter(name__iexact=name).exists():
            messages.error(request, "A collection with that name already exists.")
            return render(request, 'accounts/create_collection.html')

        # Create a collection
        Collection.objects.create(name=name, description=description)
        messages.success(request, f"Collection '{name}' created successfully.")
        return redirect('accounts:manager_dashboard')

    return render(request, 'accounts/create_collection.html')

# Delete collection
@login_required(login_url='accounts:web_login')
def delete_collection(request, collection_id):
    if request.user.role != 'MANAGER':
        messages.error(request, "You don't have permission to delete collections.")
        return redirect('accounts:dashboard')

    collection = get_object_or_404(Collection, pk=collection_id)
    collection_name = collection.name
    collection.delete()
    messages.success(request, f"Collection '{collection_name}' was deleted successfully.")
    return redirect('accounts:manager_dashboard')
