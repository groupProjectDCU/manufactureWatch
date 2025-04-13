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
        messages.error(request, "You don't have permission to create a fault case.")
        return redirect('home')  # Redirect to home or an appropriate page

    machine = None  # Placeholder if machine data is missing
    if request.method == 'POST':
        form = FaultCaseForm(request.POST, request.FILES)  # Include files in form submission
        note = request.POST.get('note')  # Get the note from the POST data
        fault_image = request.FILES.get('fault_image')  # Get the uploaded image
        machine_id = request.POST.get('machine')  # Get the selected machine

        # Validate the form data
        if form.is_valid():
            fault = form.save(commit=False)  # Create a new FaultCase instance but don't save it yet
            fault.created_by = request.user  # Set the user who created the fault case
            fault.machine_id = machine_id  # Associate the fault with the selected machine
            fault.save()  # Save the fault case to the database

            # Save the uploaded image if available
            if fault_image:
                pass  # Add logic to handle the image upload if necessary

            # Create a new FaultNote
            if note:
                FaultNote.objects.create(
                    case=fault,
                    user=request.user,
                    note=note
                )

            # Update the machine status to 'FAULT'
            machine = fault.machine  # Get the machine associated with the fault
            machine.status = 'FAULT'  # Change machine status to FAULT
            machine.save()  # Save the updated machine status

            messages.success(request, f"Fault case #{fault.case_id} was successfully created.")
            return redirect('accounts:technician_dashboard')  # Redirect back to the technician dashboard after submission
    else:
        form = FaultCaseForm()  # Create an empty form for GET requests
        machine = Machinery.objects.first()  # You can modify this logic to fetch a specific machine if needed

    return render(request, 'fault_form.html', {'form': form, 'machine': machine})  # Pass the machine to the template


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

