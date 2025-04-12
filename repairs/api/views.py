from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from datetime import datetime
from ..models import FaultCase, FaultNote
import json
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes

# API Endpoints
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def repair_counts(request):
    """API endpoint to get counts of repairs by status."""
    counts = {
        'open': FaultCase.objects.filter(status='OPEN').count(),
        'in_progress': FaultCase.objects.filter(status='IN_PROGRESS').count(),
        'resolved': FaultCase.objects.filter(status='RESOLVED').count(),
    }
    return JsonResponse(counts)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def repairs_list(request):
    """API endpoint to get list of repairs, optionally filtered by status."""
    status = request.GET.get('status', 'all')
    
    repairs = FaultCase.objects.all()
    if status != 'all':
        status_map = {
            'open': 'OPEN',
            'in_progress': 'IN_PROGRESS',
            'resolved': 'RESOLVED'
        }
        if status in status_map:
            repairs = repairs.filter(status=status_map[status])
    
    repairs_data = []
    for repair in repairs:
        # Get the notes as a list if they exist
        notes = [note.note for note in repair.notes.all()] if hasattr(repair, 'notes') else []
        notes_text = "; ".join(notes) if notes else ""
        
        repairs_data.append({
            'id': repair.case_id,
            'machine_id': repair.machine.machine_id,
            'machine_name': repair.machine.name,
            'status': repair.get_status_display(),
            'details': repair.description,
            'reported_by': repair.created_by.get_full_name() if repair.created_by else 'Unknown',
            'reported_date': repair.created_at.strftime('%Y-%m-%d'),
            'resolution_notes': repair.resolution_notes,
            'notes': notes_text
        })
    
    return JsonResponse(repairs_data, safe=False)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def repair_detail(request, repair_id):
    """API endpoint to get details of a specific repair."""
    repair = get_object_or_404(FaultCase, case_id=repair_id)
    
    # Get the notes as a list if they exist
    notes = [note.note for note in repair.notes.all()] if hasattr(repair, 'notes') else []
    notes_text = "; ".join(notes) if notes else ""
    
    repair_data = {
        'id': repair.case_id,
        'machine_id': repair.machine.machine_id,
        'machine_name': repair.machine.name,
        'status': repair.get_status_display(),
        'details': repair.description,
        'reported_by': repair.created_by.get_full_name() if repair.created_by else 'Unknown',
        'reported_date': repair.created_at.strftime('%Y-%m-%d'),
        'resolution_notes': repair.resolution_notes,
        'notes': notes_text
    }
    
    return JsonResponse(repair_data)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def repair_complete(request, repair_id):
    """API endpoint to mark a repair as completed."""
    repair = get_object_or_404(FaultCase, case_id=repair_id)
    repair.status = 'RESOLVED'
    repair.resolved_at = datetime.now()
    repair.save()
    return JsonResponse({'status': 'success'})

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def repair_start(request, repair_id):
    """API endpoint to mark a repair as in progress."""
    repair = get_object_or_404(FaultCase, case_id=repair_id)
    repair.status = 'IN_PROGRESS'
    repair.save()
    return JsonResponse({'status': 'success'})

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def repair_update(request, repair_id):
    """API endpoint to update repair details and add notes."""
    
    repair = get_object_or_404(FaultCase, case_id=repair_id)
    
    # Use request.data from DRF instead of manually parsing JSON
    data = request.data
    
    # Handle notes field
    if 'notes' in data and data['notes'].strip():
        note_text = data['notes']
        
        # Create a FaultNote entry to track history
        FaultNote.objects.create(
            case=repair,
            user=request.user if request.user.is_authenticated else None,
            note=note_text
        )
        
        success = True
        message = "Note added successfully"
    # Also maintain backward compatibility with resolution_notes field
    elif 'resolution_notes' in data and data['resolution_notes'].strip():
        # Update resolution notes on the repair
        repair.resolution_notes = data['resolution_notes'] 
        repair.save()
        
        # Also create a FaultNote entry to track history
        FaultNote.objects.create(
            case=repair,
            user=request.user if request.user.is_authenticated else None,
            note=data['resolution_notes']
        )
        
        success = True
        message = "Resolution notes updated successfully"
    else:
        success = False
        message = "No valid notes provided"
    
    # Handle file uploads if any
    if request.FILES:
        # Since there's no direct field for images, we'd need to implement
        # proper file handling here or use a third-party solution
        pass
    
    return JsonResponse({
        'success': success,
        'message': message
    }) 