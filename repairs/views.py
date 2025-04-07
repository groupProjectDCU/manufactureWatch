from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import FaultCase, FaultNote
from .forms import FaultCaseForm, FaultNoteForm, FaultUpdateForm

# TODO: UNCOMMENT LOGIN DECORATORS WHEN AUTHORIZATION IS IMPLEMENTED ON BACK-END
# @login_required
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

# @login_required
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

# @login_required
def fault_case_create(request):
    """
    View to create a new fault case.
    - Only technicians can create a fault case.
    - Handles both GET and POST requests.
    - On GET, displays an empty form for creating a new fault case.
    - On POST, validates the form data and saves the new fault case to the database. Redirects to the detail view of the newly created fault case.
    - Passes the form to the 'fault_form.html' template for rendering.
    """

    # TODO: add technician access
    # if not request.user.role == 'TECHNICIAN': # Check if the user is a technician
        # If the user is not a technician, redirect to the fault case list page
    #    return render(request, '403.html', status=403) # Render a 403 Forbidden page
    
    if request.method == 'POST':
        form = FaultCaseForm(request.POST) # Bind the submitted data to the form
        # Validate the form data
        if form.is_valid():
            fault = form.save(commit=False) # Create a new FaultCase instance but don't save it yet
            fault.created_by = request.user # Set the user who created the fault case
            fault.save() # Save the fault case to the database

            # Fetch related notes for the fault case
            notes = FaultNote.objects.filter(fault_case=fault).order_by('-created_at') # Fetch all notes related to the fault case

            return render(request, 'fault_detail.html', {'fault_case': fault, 'notes': notes}) # Render the fault detail directly.
    else:
        form = FaultCaseForm() # Create an empty form for GET requests

    return render(request, 'fault_form.html', {'form': form}) # Render the form template

# @login_required
def fault_case_update(request, fault_case_id):
    """
    View to update an existing fault case.
    - Handles both GET and POST requests.
    - On GET, displays a form pre-filled with the fault case's current data.
    - On POST, validates the form data and updates the fault case in the database. Redirects to the detail view of the updated fault case.
    - Passes the form to the 'fault_form.html' template for rendering.
    """
    fault = get_object_or_404(FaultCase, case_id=fault_case_id) # Get the fault case by ID or return a 404 error if not found.
    if request.method == 'POST':
        form = FaultUpdateForm(request.POST, instance=fault) # Bind the submitted data to the form and specify the instance to update
        # Validate the form data
        if form.is_valid():
            form.save() # Save the updated fault case to the database
            return redirect('fault_case_detail', case_id=fault_case_id) # Redirect to the detail view of the updated fault case
    else:
        form = FaultUpdateForm(instance=fault) # Create a form pre-filled with the fault case's current data for GET requests
    return render(request, 'fault_form.html', {'form': form}) # Render the form template

# @login_required
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
