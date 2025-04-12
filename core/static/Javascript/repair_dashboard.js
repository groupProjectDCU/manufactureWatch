document.addEventListener('DOMContentLoaded', function() {
    // Initialize variables
    let currentFilter = 'all';
    const repairModal = new bootstrap.Modal(document.getElementById('repairDetailsModal'));
    const repairDetailsModal = document.getElementById('repairDetailsModal');
    
    // Store the element that had focus before the modal was opened
    let previouslyFocusedElement = null;
    
    // Function to fetch and update repair counts
    function updateRepairCounts() {
        fetch('/api/repairs/counts/')
            .then(response => response.json())
            .then(data => {
                document.getElementById('open-count').textContent = data.open || 0;
                document.getElementById('in-progress-count').textContent = data.in_progress || 0;
                document.getElementById('resolved-count').textContent = data.resolved || 0;
            })
            .catch(error => console.error('Error fetching repair counts:', error));
    }

    // Function to fetch and update repairs table
    function updateRepairsTable(status = 'all') {
        const url = status === 'all' ? '/api/repairs/' : `/api/repairs/?status=${status}`;
        fetch(url)
            .then(response => response.json())
            .then(repairs => {
                const tbody = document.getElementById('repairs-tbody');
                tbody.innerHTML = '';
                
                repairs.forEach(repair => {
                    const tr = document.createElement('tr');
                    
                    // Define action buttons based on repair status
                    let actionButtons = '';
                    
                    if (repair.status.toLowerCase() === 'open') {
                        actionButtons = `
                            <button class="btn btn-sm btn-warning start-repair-btn" data-repair-id="${repair.id}">
                                Start Repair
                            </button>
                            <button class="btn btn-sm btn-info update-notes-btn" data-repair-id="${repair.id}">
                                Update Notes
                            </button>
                        `;
                    } else if (repair.status.toLowerCase() === 'in progress') {
                        actionButtons = `
                            <button class="btn btn-sm btn-success mark-repaired-btn" data-repair-id="${repair.id}">
                                Mark as Resolved
                            </button>
                            <button class="btn btn-sm btn-info update-notes-btn" data-repair-id="${repair.id}">
                                Update Notes
                            </button>
                        `;
                    } else if (repair.status.toLowerCase() === 'resolved') {
                        actionButtons = `
                            <button class="btn btn-sm btn-info update-notes-btn" data-repair-id="${repair.id}">
                                View Details
                            </button>
                        `;
                    }
                    
                    tr.innerHTML = `
                        <td>${repair.id}</td>
                        <td>${repair.machine_id}</td>
                        <td>${repair.machine_name}</td>
                        <td><span class="badge bg-${getStatusBadgeClass(repair.status)}">${repair.status}</span></td>
                        <td>${repair.details}</td>
                        <td>${repair.reported_by}</td>
                        <td>${repair.reported_date}</td>
                        <td>
                            ${actionButtons}
                        </td>
                    `;
                    tbody.appendChild(tr);
                });
            })
            .catch(error => console.error('Error fetching repairs:', error));
    }

    // Helper function to get badge class based on status
    function getStatusBadgeClass(status) {
        switch(status.toLowerCase()) {
            case 'open':
                return 'danger';
            case 'in_progress':
                return 'warning';
            case 'resolved':
                return 'success';
            default:
                return 'secondary';
        }
    }

    // Event listener for status card clicks
    document.querySelectorAll('.status-card').forEach(card => {
        card.addEventListener('click', function() {
            const status = this.dataset.status;
            currentFilter = status;
            updateRepairsTable(status);
            
            // Update active state of cards
            document.querySelectorAll('.status-card').forEach(c => {
                c.classList.remove('border-4', 'active');
            });
            this.classList.add('border-4', 'active');
            
            // Update the table header
            const tableHeading = document.querySelector('h4.mb-3');
            if (tableHeading) {
                if (status === 'all') {
                    tableHeading.textContent = 'All Repairs';
                } else {
                    // Format the status text for display
                    const formattedStatus = status === 'in_progress' ? 
                        'In Progress' : status.charAt(0).toUpperCase() + status.slice(1);
                    tableHeading.textContent = `${formattedStatus} Repairs`;
                }
            }
        });
    });

    // Event delegation for table row buttons
    document.getElementById('repairs-tbody').addEventListener('click', function(e) {
        if (e.target.classList.contains('update-notes-btn')) {
            const repairId = e.target.dataset.repairId;
            // Fetch repair details and show modal
            fetch(`/api/repairs/${repairId}/`)
                .then(response => response.json())
                .then(repair => {
                    // Update modal with repair details
                    document.getElementById('repairId').value = repair.id;
                    document.getElementById('partsUsed').value = ''; // No parts_used field
                    
                    // Display previous notes if any
                    let previousNotesHtml = '';
                    if (repair.notes) {
                        previousNotesHtml = `
                            <div class="mb-3">
                                <label class="form-label">Previous Notes</label>
                                <div class="form-control bg-light" style="height: auto; min-height: 100px; overflow-y: auto;">
                                    ${repair.notes.replace(/\n/g, '<br>').replace(/;/g, '<hr class="my-2">')}
                                </div>
                            </div>
                        `;
                    }
                    
                    document.getElementById('previousNotesContainer').innerHTML = previousNotesHtml;
                    
                    // Clear the new note field
                    document.getElementById('repairNotes').value = '';
                    
                    // Update modal title and form fields based on status
                    const modalTitle = document.querySelector('#repairDetailsModal .modal-title');
                    const notesTextarea = document.getElementById('repairNotes');
                    const notesContainer = document.querySelector('#repairDetailsForm .mb-3:nth-child(3)');
                    const submitButton = document.getElementById('submitRepairUpdate');
                    const partsUsedContainer = document.querySelector('#repairDetailsForm .mb-3:nth-child(1)');
                    
                    if (repair.status.toLowerCase() === 'resolved') {
                        // For resolved repairs - show resolution notes if available
                        modalTitle.textContent = 'Repair Details (Resolved)';
                        submitButton.style.display = 'none';
                        notesContainer.style.display = 'none';
                        
                        // Show resolution notes if available
                        if (repair.resolution_notes) {
                            let resolutionNotesHtml = `
                                <div class="mb-3">
                                    <label class="form-label">Resolution Notes</label>
                                    <div class="form-control bg-light" style="height: auto; min-height: 100px; overflow-y: auto;">
                                        ${repair.resolution_notes.replace(/\n/g, '<br>')}
                                    </div>
                                </div>
                            `;
                            // Add resolution notes to the container
                            document.getElementById('previousNotesContainer').innerHTML += resolutionNotesHtml;
                        }
                        
                        // Show parts used if available
                        if (repair.parts_used) {
                            document.getElementById('partsUsed').value = repair.parts_used;
                        }
                        document.getElementById('partsUsed').disabled = true;
                        
                    } else {
                        // For open or in_progress repairs
                        modalTitle.textContent = repair.status === 'open' ? 'Update Open Repair' : 'Update In-Progress Repair';
                        submitButton.style.display = 'block';
                        notesContainer.style.display = 'block';
                        
                        // Enable parts used field
                        document.getElementById('partsUsed').value = repair.parts_used || '';
                        document.getElementById('partsUsed').disabled = false;
                    }
                    
                    repairModal.show();
                })
                .catch(error => console.error('Error fetching repair details:', error));
        } else if (e.target.classList.contains('mark-repaired-btn')) {
            const repairId = e.target.dataset.repairId;
            if (confirm('Are you sure you want to mark this repair as resolved?')) {
                fetch(`/api/repairs/${repairId}/complete/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCsrfToken()
                    }
                })
                .then(response => {
                    if (response.ok) {
                        updateRepairCounts();
                        updateRepairsTable(currentFilter);
                    }
                })
                .catch(error => console.error('Error marking repair as resolved:', error));
            }
        } else if (e.target.classList.contains('start-repair-btn')) {
            const repairId = e.target.dataset.repairId;
            if (confirm('Are you sure you want to start working on this repair?')) {
                fetch(`/api/repairs/${repairId}/start/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCsrfToken()
                    }
                })
                .then(response => {
                    if (response.ok) {
                        updateRepairCounts();
                        updateRepairsTable(currentFilter);
                    }
                })
                .catch(error => console.error('Error starting repair process:', error));
            }
        }
    });

    // Store element that had focus before modal opens
    repairDetailsModal.addEventListener('show.bs.modal', function() {
        previouslyFocusedElement = document.activeElement;
    });

    // Direct fix for the aria-hidden accessibility issue
    repairDetailsModal.addEventListener('hide.bs.modal', function(event) {
        // When the modal starts to hide, immediately set the inert attribute
        // This prevents focus and accessibility issues during the closing animation
        repairDetailsModal.setAttribute('inert', '');
        
        // Remove inert after the modal is fully hidden
        repairDetailsModal.addEventListener('hidden.bs.modal', function onHidden() {
            repairDetailsModal.removeAttribute('inert');
            repairDetailsModal.removeEventListener('hidden.bs.modal', onHidden);
            
            // Return focus to a safe element
            if (previouslyFocusedElement && previouslyFocusedElement.focus) {
                try {
                    previouslyFocusedElement.focus();
                } catch (e) {
                    document.body.focus();
                }
            } else {
                document.body.focus();
            }
        }, { once: true });
    });
    
    // Stop the close buttons from maintaining focus
    document.querySelector('#repairDetailsModal .btn-close').addEventListener('mousedown', function(e) {
        // Prevent the default behavior that would focus the button
        e.preventDefault();
        // Close the modal programmatically
        repairModal.hide();
    }, true);
    
    // Intercept Escape key to implement custom closing behavior
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && repairDetailsModal.classList.contains('show')) {
            e.preventDefault(); // Prevent Bootstrap's default Escape handling
            repairDetailsModal.setAttribute('inert', ''); // Set inert immediately
            repairModal.hide(); // Then close the modal
        }
    }, true);

    document.getElementById('submitRepairUpdate').addEventListener('click', function() {
        // Blur this button and any other active elements before processing
        this.blur();
        document.activeElement.blur();
        document.body.focus();
        
        const repairId = document.getElementById('repairId').value;
        const notes = document.getElementById('repairNotes').value;
        
        if (!notes.trim()) {
            alert('Please enter a note before saving');
            return;
        }
        
        fetch(`/api/repairs/${repairId}/update/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({
                notes: notes  // Changed from resolution_notes to notes
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to update repair notes');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                // Show success message
                alert('Notes updated successfully');
                repairModal.hide();
                updateRepairsTable(currentFilter);
            } else {
                alert(data.message || 'Failed to update notes');
            }
        })
        .catch(error => {
            console.error('Error updating repair:', error);
            alert('Error updating repair notes. Please try again.');
        });
    });

    // Helper function to get CSRF token
    function getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }

    // Initial load
    updateRepairCounts();
    updateRepairsTable();

    // Set up periodic updates
    setInterval(updateRepairCounts, 30000); // Update counts every 30 seconds
    setInterval(() => updateRepairsTable(currentFilter), 30000); // Update table every 30 seconds
}); 