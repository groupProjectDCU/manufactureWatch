from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import FaultCase, FaultNote
from .forms import FaultCaseForm, FaultNoteForm, FaultUpdateForm
from . import urls

@login_required
def fault_case_list(request):
    """View to list all fault cases."""
    faults = FaultCase.objects.all().order_by('-created_at')
    for fault in faults:
        fault.days_open = (datetime.now().date() - fault.created_at.date()).days
    return render(request, 'repairs/fault_list.html', {'faults': faults})

@login_required
def fault_case_detail(request, case_id):
    """View to display details of a specific fault case."""
    fault = get_object_or_404(FaultCase, id=case_id)
    fault.days_open = (datetime.now().date() - fault.created_at.date()).days
    notes = FaultNote.objects.filter(fault_case=fault).order_by('-created_at')
    return render(request, 'repairs/fault_detail.html', {'fault_case': fault, 'notes': notes})

@login_required
def fault_case_create(request):
    """View to create a new fault case."""
    if request.method == 'POST':
        form = FaultCaseForm(request.POST)
        if form.is_valid():
            fault = form.save(commit=False)
            fault.created_by = request.user
            fault.save()
            return redirect('fault_case_detail', case_id=fault.id)
    else:
        form = FaultCaseForm()
    return render(request, 'repairs/fault_form.html', {'form': form})

@login_required
def fault_case_update(request, case_id):
    """View to update an existing fault case."""
    fault = get_object_or_404(FaultCase, id=case_id)
    if request.method == 'POST':
        form = FaultUpdateForm(request.POST, instance=fault)
        if form.is_valid():
            form.save()
            return redirect('fault_case_detail', case_id=fault.id)
    else:
        form = FaultUpdateForm(instance=fault)
    return render(request, 'repairs/fault_form.html', {'form': form})

@login_required
def fault_note_create(request, case_id):
    """View to create a new note for a fault case."""
    fault = get_object_or_404(FaultCase, id=case_id)
    if request.method == 'POST':
        form = FaultNoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.fault = fault
            note.created_by = request.user
            note.save()
            return redirect('fault_case_detail', case_id=fault.id)
    else:
        form = FaultNoteForm()
    return render(request, 'repairs/note_form.html', {'form': form, 'fault_case': fault})
