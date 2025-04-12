document.addEventListener('DOMContentLoaded', function() {
    // Initialize modals
    const machineDetailsModal = new bootstrap.Modal(document.getElementById('machineDetailsModal'));
    const repairModal = new bootstrap.Modal(document.getElementById('repairModal'));
    
    // Store current machine ID and repair ID
    let currentMachineId = null;
    let currentRepairId = null;
    let previouslyFocusedElement = null;
    let currentStatusFilter = 'ALL'; // Track current filter status
    
    // Start real-time updates for count cards
    startRealTimeUpdates();
    
    // Set up event listeners
    initEventListeners();
    
    // Function to start periodic updates of count cards
    function startRealTimeUpdates() {
        // Fetch counts immediately on page load
        fetchMachineCounts();
        
        // Then fetch counts every 30 seconds
        setInterval(fetchMachineCounts, 30000);
    }
    
    // Function to fetch machine counts from the server
    function fetchMachineCounts() {
        fetch('/api/machinery/counts/', {
            headers: {
                'X-CSRFToken': getCsrfToken(),
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            credentials: 'same-origin'
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            // Update the count display
            document.getElementById('ok-count').textContent = data.ok_count;
            document.getElementById('warning-count').textContent = data.warning_count;
            document.getElementById('fault-count').textContent = data.fault_count;
            document.getElementById('total-count').textContent = data.total_count;
        })
        .catch(error => {
            console.error('Error fetching machine counts:', error);
        });
    }
    
    function initEventListeners() {
        // Handle status card clicks for filtering
        document.querySelectorAll('.status-card').forEach(card => {
            card.addEventListener('click', function() {
                const status = this.dataset.status;
                currentStatusFilter = status;
                
                // Highlight the selected card
                document.querySelectorAll('.status-card').forEach(c => {
                    c.classList.remove('border-5', 'border-white', 'active');
                });
                this.classList.add('border-5', 'border-white', 'active');
                
                // Filter table based on status
                filterMachineTable(status);
            });
        });
        
        // Handle machine row clicks
        document.querySelectorAll('.machine-row').forEach(row => {
            row.addEventListener('click', function() {
                const machineId = this.dataset.machineId;
                currentMachineId = machineId;
                loadMachineDetails(machineId);
                machineDetailsModal.show();
            });
        });
        
        // Handle direct history button clicks in the table
        document.querySelectorAll('.view-history-btn').forEach(btn => {
            btn.addEventListener('click', function(e) {
                // Stop the event from bubbling up to the row click handler
                e.stopPropagation();
                
                const machineId = this.dataset.machineId;
                currentMachineId = machineId;
                
                // Reset the repair notes content
                document.getElementById('repairNotesContent').innerHTML = `
                    <div class="text-center py-5">
                        <p class="text-muted">Select a repair from the history tab to view its notes</p>
                    </div>
                `;
                
                // Show history tab and load repair history
                const historyTab = document.querySelector('#history-tab');
                historyTab.click();
                loadRepairHistory(machineId);
                repairModal.show();
            });
        });
        
        // Handle view repair history button in details modal
        const viewRepairHistoryBtn = document.getElementById('viewRepairHistoryBtn');
        if (viewRepairHistoryBtn) {
            viewRepairHistoryBtn.addEventListener('click', function() {
                if (currentMachineId) {
                    // Reset the repair notes content
                    document.getElementById('repairNotesContent').innerHTML = `
                        <div class="text-center py-5">
                            <p class="text-muted">Select a repair from the history tab to view its notes</p>
                        </div>
                    `;
                    
                    // Show history tab and load repair history
                    const historyTab = document.querySelector('#history-tab');
                    historyTab.click();
                    loadRepairHistory(currentMachineId);
                    repairModal.show();
                }
            });
        }
        
        // Handle edit machine button
        const editMachineBtn = document.getElementById('editMachineBtn');
        if (editMachineBtn) {
            editMachineBtn.addEventListener('click', function() {
                if (currentMachineId) {
                    window.location.href = `/accounts/dashboard/manager/machines/${currentMachineId}/edit/`;
                }
            });
        }
        
        // Handle modal hidden events to maintain filter state
        const modalElements = [
            document.getElementById('machineDetailsModal'),
            document.getElementById('repairModal')
        ];
        
        modalElements.forEach(modalElement => {
            if (modalElement) {
                modalElement.addEventListener('hidden.bs.modal', function() {
                    // Re-apply the current filter when any modal is closed
                    if (currentStatusFilter !== 'ALL') {
                        filterMachineTable(currentStatusFilter);
                    }
                });
            }
        });
        
        // Improved modal accessibility fixes
        setupModalAccessibility();
    }
    
    // Function to filter the machine table based on status
    function filterMachineTable(status) {
        const machineRows = document.querySelectorAll('.machine-row');
        const tableContainer = document.querySelector('.card-body .table-responsive');
        
        let visibleCount = 0;
        
        machineRows.forEach(row => {
            // Find the status badge inside the row
            const statusBadge = row.querySelector('td:nth-child(5) .badge');
            if (!statusBadge) return;
            
            const machineStatus = statusBadge.textContent.trim().toUpperCase();
            
            if (status === 'ALL' || machineStatus === status) {
                row.style.display = '';
                visibleCount++;
            } else {
                row.style.display = 'none';
            }
        });
        
        // Update the table header to show what we're filtering by
        const tableHeader = document.querySelector('.card-header span');
        if (tableHeader) {
            if (status === 'ALL') {
                tableHeader.textContent = 'Machinery Status';
            } else {
                tableHeader.textContent = `Machinery Status (${status.charAt(0) + status.slice(1).toLowerCase()} Only)`;
            }
        }
        
        // Show a message if no results
        if (visibleCount === 0 && tableContainer) {
            // Check if we already have a "no results" message
            let noResultsMsg = tableContainer.querySelector('.no-results-message');
            
            if (!noResultsMsg) {
                // Create the message if it doesn't exist
                noResultsMsg = document.createElement('div');
                noResultsMsg.className = 'alert alert-info no-results-message mt-3';
                tableContainer.appendChild(noResultsMsg);
            }
            
            noResultsMsg.textContent = `No machines with ${status.toLowerCase()} status found.`;
            noResultsMsg.style.display = 'block';
        } else if (tableContainer) {
            // Hide the message if we have results
            const noResultsMsg = tableContainer.querySelector('.no-results-message');
            if (noResultsMsg) {
                noResultsMsg.style.display = 'none';
            }
        }
    }
    
    function setupModalAccessibility() {
        // Accessibility fix for the machineDetailsModal
        const machineDetailsModalElement = document.getElementById('machineDetailsModal');
        if (machineDetailsModalElement) {
            machineDetailsModalElement.addEventListener('show.bs.modal', function() {
                previouslyFocusedElement = document.activeElement;
            });
            
            machineDetailsModalElement.addEventListener('hide.bs.modal', function(event) {
                this.setAttribute('inert', '');
                
                this.addEventListener('hidden.bs.modal', function onHidden() {
                    this.removeAttribute('inert');
                    this.removeEventListener('hidden.bs.modal', onHidden);
                    
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
        }
        
        // Similar handling for repairModal
        const repairModalElement = document.getElementById('repairModal');
        if (repairModalElement) {
            repairModalElement.addEventListener('hide.bs.modal', function(event) {
                this.setAttribute('inert', '');
                this.addEventListener('hidden.bs.modal', function onHidden() {
                    this.removeAttribute('inert');
                    this.removeEventListener('hidden.bs.modal', onHidden);
                }, { once: true });
            });
        }
    }
    
    // Function to load machine details
    function loadMachineDetails(machineId) {
        const detailsContainer = document.getElementById('machineDetailsContent');
        if (!detailsContainer) return;
        
        detailsContainer.innerHTML = `
            <div class="text-center">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </div>
        `;
        
        // Fetch machine details from server
        fetch(`/api/machinery/${machineId}/details/`, {
            headers: {
                'X-CSRFToken': getCsrfToken(),
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            credentials: 'same-origin'
        })
        .then(response => {
            if (!response.ok) {
                if (response.status === 401) {
                    throw new Error("Authentication failed. You may need to log in again.");
                } else if (response.status === 404) {
                    throw new Error("The machine details endpoint was not found. Check your API configuration.");
                } else {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
            }
            return response.json();
        })
        .then(machine => {
            // Format the details into a nice card with safe handling of potentially missing fields
            detailsContainer.innerHTML = `
                <div class="row">
                    <div class="col-md-6">
                        <h4>${machine.name || 'Unnamed Machine'}</h4>
                        <p class="text-muted">ID: ${machine.machine_id}</p>
                        <p><strong>Model:</strong> ${machine.model || '—'}</p>
                        <p><strong>Status:</strong> <span class="badge bg-${getStatusClass(machine.status)}">${machine.status || 'Unknown'}</span></p>
                        <p><strong>Priority:</strong> ${getPriorityLabel(machine.priority || 0)}</p>
                    </div>
                    <div class="col-md-6">
                        <h5>Description</h5>
                        <p>${machine.description || 'No description available.'}</p>
                        <p><strong>Last Maintained:</strong> ${machine.last_maintained || 'No record'}</p>
                        <p><strong>Created At:</strong> ${machine.created_at ? formatDate(machine.created_at) : 'No record'}</p>
                        <p><strong>Updated At:</strong> ${machine.updated_at ? formatDate(machine.updated_at) : 'No record'}</p>
                    </div>
                </div>
            `;
        })
        .catch(error => {
            detailsContainer.innerHTML = `
                <div class="alert alert-danger">
                    Error loading machine details: ${error.message}
                    <br>
                    <small>Please make sure the API endpoint is properly configured.</small>
                </div>
            `;
        });
    }
    
    // Function to load repair history
    function loadRepairHistory(machineId) {
        const historyContainer = document.getElementById('repairHistoryContent');
        if (!historyContainer) return;
        
        historyContainer.innerHTML = `
            <div class="text-center">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </div>
        `;
        
        // Fetch repair history from server
        fetch(`/api/machinery/${machineId}/repairs/`, {
            headers: {
                'X-CSRFToken': getCsrfToken(),
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            credentials: 'same-origin'
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(repairs => {
            if (repairs.length === 0) {
                historyContainer.innerHTML = `
                    <div class="alert alert-info">
                        No repair history found for this machine.
                    </div>
                `;
                return;
            }
            
            // Create table with repair history
            let tableHtml = `
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>Repair ID</th>
                            <th>Status</th>
                            <th>Details</th>
                            <th>Reported By</th>
                            <th>Reported Date</th>
                            <th>Resolved Date</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
            `;
            
            repairs.forEach(repair => {
                tableHtml += `
                    <tr>
                        <td>${repair.id}</td>
                        <td><span class="badge bg-${getRepairStatusClass(repair.status)}">${repair.status}</span></td>
                        <td>${repair.details}</td>
                        <td>${repair.reported_by}</td>
                        <td>${repair.reported_date}</td>
                        <td>${repair.resolved_date || '—'}</td>
                        <td>
                            <button class="btn btn-sm btn-info view-notes-btn" data-repair-id="${repair.id}">
                                View Notes
                            </button>
                        </td>
                    </tr>
                `;
            });
            
            tableHtml += `
                    </tbody>
                </table>
            `;
            
            historyContainer.innerHTML = tableHtml;
            
            // Add event listeners to view notes buttons
            document.querySelectorAll('.view-notes-btn').forEach(btn => {
                btn.addEventListener('click', function() {
                    const repairId = this.dataset.repairId;
                    currentRepairId = repairId;
                    loadRepairNotes(repairId);
                    
                    // Switch to the notes tab
                    const notesTab = document.querySelector('#notes-tab');
                    notesTab.click();
                });
            });
        })
        .catch(error => {
            historyContainer.innerHTML = `
                <div class="alert alert-danger">
                    Error loading repair history: ${error.message}
                    <br>
                    <small>Please make sure the API endpoint is properly configured.</small>
                </div>
            `;
        });
    }
    
    // Function to load repair notes
    function loadRepairNotes(repairId) {
        const notesContainer = document.getElementById('repairNotesContent');
        if (!notesContainer) return;
        
        notesContainer.innerHTML = `
            <div class="text-center">
                <div class="spinner-border text-info" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </div>
        `;
        
        // Fetch repair details including notes
        fetch(`/api/repairs/${repairId}/`, {
            headers: {
                'X-CSRFToken': getCsrfToken(),
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            credentials: 'same-origin'
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(repair => {
            let notesHtml = `
                <div class="card mb-3">
                    <div class="card-header bg-info text-white">
                        <h5 class="card-title mb-0">Repair #${repair.id}</h5>
                    </div>
                    <div class="card-body">
            `;
            
            // Resolution notes
            if (repair.resolution_notes) {
                notesHtml += `
                    <div class="mb-3">
                        <h5>Resolution Notes</h5>
                        <div class="p-3 bg-light rounded">
                            ${repair.resolution_notes.replace(/\n/g, '<br>')}
                        </div>
                    </div>
                `;
            }
            
            // All notes history
            if (repair.notes) {
                notesHtml += `
                    <div class="mb-3">
                        <h5>Notes History</h5>
                        <div class="notes-timeline">
                `;
                
                const notesList = repair.notes.split(';');
                notesList.forEach(note => {
                    if (note.trim()) {
                        notesHtml += `
                            <div class="note-item p-2 border-bottom">
                                <p>${note.trim()}</p>
                            </div>
                        `;
                    }
                });
                
                notesHtml += `
                        </div>
                    </div>
                `;
            }
            
            if (!repair.resolution_notes && !repair.notes) {
                notesHtml += `
                    <div class="alert alert-info">
                        No notes available for this repair.
                    </div>
                `;
            }
            
            notesHtml += `
                    </div>
                </div>
                <button class="btn btn-secondary btn-sm" id="backToHistoryBtn">
                    <i class="bi bi-arrow-left"></i> Back to Repair History
                </button>
            `;
            
            notesContainer.innerHTML = notesHtml;
            
            // Add event listener to the back button
            const backToHistoryBtn = document.getElementById('backToHistoryBtn');
            if (backToHistoryBtn) {
                backToHistoryBtn.addEventListener('click', function() {
                    // Switch back to the history tab
                    const historyTab = document.querySelector('#history-tab');
                    historyTab.click();
                });
            }
        })
        .catch(error => {
            notesContainer.innerHTML = `
                <div class="alert alert-danger">
                    Error loading repair notes: ${error.message}
                    <br>
                    <small>Please make sure the API endpoint is properly configured.</small>
                </div>
            `;
        });
    }
    
    // Helper function to get CSRF token
    function getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }
    
    // Helper function to get status badge class
    function getStatusClass(status) {
        switch(status) {
            case 'OK': return 'success';
            case 'WARNING': return 'warning';
            case 'FAULT': return 'danger';
            default: return 'secondary';
        }
    }
    
    // Helper function to get repair status badge class
    function getRepairStatusClass(status) {
        switch(status.toLowerCase()) {
            case 'open': return 'danger';
            case 'in_progress': return 'warning';
            case 'resolved': return 'success';
            default: return 'secondary';
        }
    }
    
    // Helper function to get priority label
    function getPriorityLabel(priority) {
        if (priority >= 7) return '<span class="badge bg-danger">High</span>';
        if (priority >= 4) return '<span class="badge bg-warning text-dark">Medium</span>';
        return '<span class="badge bg-secondary">Low</span>';
    }
    
    // Helper function to format date
    function formatDate(dateString) {
        if (!dateString) return '—';
        const date = new Date(dateString);
        return date.toLocaleDateString();
    }
}); 