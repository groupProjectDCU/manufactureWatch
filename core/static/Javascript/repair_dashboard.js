document.addEventListener('DOMContentLoaded', function() {
    // Initialize variables
    let currentFilter = 'all';
    const repairModal = new bootstrap.Modal(document.getElementById('repairDetailsModal'));
    
    // Function to fetch and update repair counts
    function updateRepairCounts() {
        fetch('/api/repairs/counts/')
            .then(response => response.json())
            .then(data => {
                document.getElementById('pending-count').textContent = data.pending || 0;
                document.getElementById('in-progress-count').textContent = data.in_progress || 0;
                document.getElementById('completed-count').textContent = data.completed || 0;
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
                    tr.innerHTML = `
                        <td>${repair.id}</td>
                        <td>${repair.machine_id}</td>
                        <td>${repair.machine_name}</td>
                        <td><span class="badge bg-${getStatusBadgeClass(repair.status)}">${repair.status}</span></td>
                        <td>${repair.details}</td>
                        <td>${repair.reported_by}</td>
                        <td>${repair.reported_date}</td>
                        <td>
                            <button class="btn btn-sm btn-success mark-repaired-btn" data-repair-id="${repair.id}">
                                Mark as Repaired
                            </button>
                            <button class="btn btn-sm btn-info update-notes-btn" data-repair-id="${repair.id}">
                                Update Notes
                            </button>
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
            case 'pending':
                return 'danger';
            case 'in_progress':
                return 'warning';
            case 'completed':
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
                c.classList.remove('border-4');
            });
            this.classList.add('border-4');
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
                    document.getElementById('repairId').value = repair.id;
                    document.getElementById('partsUsed').value = repair.parts_used || '';
                    document.getElementById('repairNotes').value = repair.notes || '';
                    repairModal.show();
                })
                .catch(error => console.error('Error fetching repair details:', error));
        } else if (e.target.classList.contains('mark-repaired-btn')) {
            const repairId = e.target.dataset.repairId;
            if (confirm('Are you sure you want to mark this repair as completed?')) {
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
                .catch(error => console.error('Error marking repair as completed:', error));
            }
        }
    });

    // Handle repair details form submission
    document.getElementById('saveRepairDetails').addEventListener('click', function() {
        const formData = new FormData(document.getElementById('repairDetailsForm'));
        const repairId = formData.get('repairId');

        fetch(`/api/repairs/${repairId}/update/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCsrfToken()
            }
        })
        .then(response => {
            if (response.ok) {
                repairModal.hide();
                updateRepairsTable(currentFilter);
            }
        })
        .catch(error => console.error('Error updating repair details:', error));
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