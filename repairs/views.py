from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib import messages

from machinery.models import Machinery
from .models import FaultCase, FaultNote
from .forms import FaultCaseForm, FaultNoteForm, FaultUpdateForm

@login_required
def fault_case_list(request):
    """
    View to list all fault cases.
    - Fetches all fault cases from the database, ordered by creation date.
    - Calculates the number of days each fault case has been open.
    - Passes the fault cases to the 'fault_list.html' template for rendering.
    """
    faults = FaultCase.objects.all().order_by('-created_at')
    for fault in faults:
        # Calculate the number of days the fault case has been open
        fault.days_open = (datetime.now().date() - fault.created_at.date()).days
    return render(request, 'fault_list.html', {'faults': faults}) # Render the list of faults

@login_required
def fault_case_detail(request, fault_case_id):
    """
    View to display details of a specific fault case.
    - Fetches the fault case by ID
    - Calculates the number of days it has been open.
    - Fetches all notes related to the fault case.
    - Passes the fault case and notes to the 'fault_detail.html' template for rendering.
    """
    fault = get_object_or_404(FaultCase, case_id=fault_case_id) # Fetch the fault case by ID
    fault.days_open = (datetime.now().date() - fault.created_at.date()).days # Calculate the number of days the fault case has been open
    notes = FaultNote.objects.filter(case=fault).order_by('-created_at') # Fetch all notes related to the fault case
    return render(request, 'fault_detail.html', {'fault_case': fault, 'notes': notes}) # Render the details of the fault case


@login_required
def fault_case_create(request):
    """
    View to create a new fault case along with a note.
    - Handles both GET and POST requests.
    - On POST, validates the form data and saves the new fault case and the fault note to the database.
    """
    if not request.user.role == 'TECHNICIAN':  # Only technicians can create a fault case
        return render(request, '403.html', status=403)  # Render a 403 Forbidden page

    if request.method == 'POST':
        form = FaultCaseForm(request.POST)  # Bind the submitted data to the form
        note = request.POST.get('note')  # Get the note from the POST data

        # Validate the form data
        if form.is_valid():
            fault = form.save(commit=False)  # Create a new FaultCase instance but don't save it yet
            fault.created_by = request.user  # Set the user who created the fault case
            fault.save()  # Save the fault case to the database

            # Update the machine's status to 'FAULT' when a fault is created
            machine = fault.machine  # Get the machine related to this fault case
            machine.status = 'FAULT'
            machine.save()

            # Create a new FaultNote
            if note:
                # Use the correct field name here
                FaultNote.objects.create(
                    case=fault,  # 'case' instead of 'fault'
                    user=request.user,
                    note=note
                )

            messages.success(request, f"Fault case #{fault.case_id} was successfully created.")
            return redirect('accounts:technician_dashboard')  # Redirect back to the technician dashboard
    else:
        form = FaultCaseForm()  # Create an empty form for GET requests

    return render(request, 'fault_form.html', {'form': form})  # Render the form template



@login_required
def fault_case_update(request, fault_case_id):
    """
    View to update an existing fault case.
    - Handles both GET and POST requests.
    - On GET, displays a form pre-filled with the fault case's current data.
    - On POST, validates the form data and updates the fault case in the database. Redirects to the detail view of the updated fault case.
    - Passes the form to the 'update_fault_form.html' template for rendering.
    """
    fault = get_object_or_404(FaultCase, case_id=fault_case_id) # Get the fault case by ID or return a 404 error if not found.
    if request.method == 'POST':
        form = FaultUpdateForm(request.POST, instance=fault) # Bind the submitted data to the form and specify the instance to update
        # Validate the form data
        if form.is_valid():
            form.save() # Save the updated fault case to the database

            messages.success(request, f"Fault case #{fault.case_id} was successfully updated.")
            return redirect('repairs:fault_case_detail', fault_case_id=fault.case_id) # Redirect to the detail view of the updated fault case
    else:
        form = FaultUpdateForm(instance=fault) # Create a form pre-filled with the fault case's current data for GET requests
    return render(request, 'update_fault_form.html', {'form': form, 'fault_case' : fault}) # Render the update form template

@login_required
def fault_note_create(request, fault_case_id):
    """
    View to create a new note for a fault case.
    - Handles both GET and POST requests.
    - On GET, displays an empty form for creating a new note.
    - On POST, validates the form data and saves the new note to the database. Redirects to the detail view of the fault case.
    - Passes the form and fault case to the 'note_form.html' template for rendering.
    """
    fault = get_object_or_404(FaultCase, case_id=fault_case_id) # Get the fault case by ID or return a 404 error if not found.
    if request.method == 'POST':
        form = FaultNoteForm(request.POST) # Bind the submitted data to the form
        # Validate the form data
        if form.is_valid():
            note = form.save(commit=False) # Create a new FaultNote instance but don't save it yet
            note.fault = fault # Associate the note with the fault case
            note.created_by = request.user # Set the user who created the note
            note.save() # Save the note to the database
            return redirect('fault_case_detail', case_id=fault_case_id) # Redirect to the detail view of the fault case
    else:
        form = FaultNoteForm() # Create an empty form for GET requests
    return render(request, 'note_form.html', {'form': form, 'fault_case': fault}) # Render the form template for creating a new note

# Add warnings (only Tech can do that)
# @login_required
# def warning_form(request, machine_id):
#     # Get the machine for which the warning is being created
#     machine = get_object_or_404(Machinery, machine_id=machine_id)
#
#     if request.method == 'POST':
#         # Process the form submission
#         message = request.POST.get('message')
#
#         # Create new warning object
#         warning = Warning.objects.create(
#             machine=machine,
#             message=message,
#             added_by=request.user,
#             is_active=True
#         )
#
#         # The Warning model's save method will automatically update the machine status
#
#         messages.success(request, f"Warning reported successfully for {machine.name}")
#         return redirect('accounts:technician_dashboard')
#
#     # Render the warning form template
#     context = {
#         'machine': machine
#     }
#     return render(request, 'warnings_form.html', context)

