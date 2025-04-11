from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from datetime import datetime
from ..models import FaultCase

# API Endpoints
@require_http_methods(["GET"])
def repair_counts(request):
    """API endpoint to get counts of repairs by status."""
    counts = {
        'pending': FaultCase.objects.filter(status='PENDING').count(),
        'in_progress': FaultCase.objects.filter(status='IN_PROGRESS').count(),
        'completed': FaultCase.objects.filter(status='COMPLETED').count(),
    }
    return JsonResponse(counts)

@require_http_methods(["GET"])
def repairs_list(request):
    """API endpoint to get list of repairs, optionally filtered by status."""
    status = request.GET.get('status', 'all')
    
    repairs = FaultCase.objects.all()
    if status != 'all':
        repairs = repairs.filter(status=status.upper())
    
    repairs_data = []
    for repair in repairs:
        repairs_data.append({
            'id': repair.case_id,
            'machine_id': repair.machine.machine_id,
            'machine_name': repair.machine.name,
            'status': repair.get_status_display(),
            'details': repair.description,
            'reported_by': repair.created_by.get_full_name() if repair.created_by else 'Unknown',
            'reported_date': repair.created_at.strftime('%Y-%m-%d'),
            'parts_used': repair.parts_used,
            'notes': repair.notes
        })
    
    return JsonResponse(repairs_data, safe=False)

@require_http_methods(["GET"])
def repair_detail(request, repair_id):
    """API endpoint to get details of a specific repair."""
    repair = get_object_or_404(FaultCase, case_id=repair_id)
    
    repair_data = {
        'id': repair.case_id,
        'machine_id': repair.machine.machine_id,
        'machine_name': repair.machine.name,
        'status': repair.get_status_display(),
        'details': repair.description,
        'reported_by': repair.created_by.get_full_name() if repair.created_by else 'Unknown',
        'reported_date': repair.created_at.strftime('%Y-%m-%d'),
        'parts_used': repair.parts_used,
        'notes': repair.notes
    }
    
    return JsonResponse(repair_data)

@require_http_methods(["POST"])
def repair_complete(request, repair_id):
    """API endpoint to mark a repair as completed."""
    repair = get_object_or_404(FaultCase, case_id=repair_id)
    repair.status = 'COMPLETED'
    repair.completed_at = datetime.now()
    repair.save()
    return JsonResponse({'status': 'success'})

@require_http_methods(["POST"])
def repair_update(request, repair_id):
    """API endpoint to update repair details."""
    repair = get_object_or_404(FaultCase, case_id=repair_id)
    
    # Update the repair with form data
    repair.parts_used = request.POST.get('partsUsed', repair.parts_used)
    repair.notes = request.POST.get('repairNotes', repair.notes)
    
    # Handle file uploads if any
    if request.FILES:
        for image in request.FILES.getlist('repairImages'):
            # Assuming you have an images field in your model
            repair.images.create(image=image)
    
    repair.save()
    return JsonResponse({'status': 'success'}) 