from django.db import models
from accounts.models import User
from machinery.models import Machinery
from django.utils import timezone
import uuid

class FaultCase(models.Model):
    STATUS_CHOICES = (
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
    )
    
    PRIORITY_CHOICES = (
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
        (4, 'Urgent'),
        (5, 'Critical'),
    )
    
    case_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    machine = models.ForeignKey(Machinery, on_delete=models.CASCADE, related_name='fault_cases')
    description = models.TextField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='OPEN')
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reported_faults')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_faults')
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='resolved_faults')
    resolution_notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"Fault {self.case_id} - {self.machine.name}"
    
    def days_open(self):
        if self.status == 'RESOLVED' and self.resolved_at:
            delta = self.resolved_at - self.created_at
        else:
            delta = timezone.now() - self.created_at
        return delta.days

class RepairLog(models.Model):
    log_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fault_case = models.ForeignKey(FaultCase, on_delete=models.CASCADE, related_name='repair_logs')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f"Log {self.log_id} for {self.fault_case}"

class FaultNote(models.Model):
    note_id = models.BigAutoField(primary_key=True)
    case = models.ForeignKey(FaultCase, on_delete=models.CASCADE, related_name='notes')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Note on Case #{self.case.case_id} by {self.user.get_full_name()}"

class Warning(models.Model):
    warning_id = models.BigAutoField(primary_key=True)
    is_active = models.BooleanField(default=True)
    machine = models.ForeignKey(Machinery, on_delete=models.CASCADE, related_name='warnings')
    message = models.TextField()
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_warnings')
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='resolved_warnings')
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Warning on {self.machine.name}: {self.message[:30]}..."
    
    def save(self, *args, **kwargs):
        # Update machine status when warning is created or resolved
        if self.is_active and self.machine.status == 'OK':
            self.machine.status = 'WARNING'
            self.machine.save()
        elif not self.is_active and self.resolved_at is None:
            from django.utils import timezone
            self.resolved_at = timezone.now()
            
            # Check if this was the only active warning for this machine
            active_warnings = Warning.objects.filter(
                machine=self.machine, 
                is_active=True
            ).exclude(pk=self.pk).count()
            
            if active_warnings == 0:
                # Check if there are active faults
                active_faults = FaultCase.objects.filter(
                    machine=self.machine,
                    status__in=['OPEN', 'IN_PROGRESS']
                ).count()
                
                if active_faults == 0:
                    self.machine.status = 'OK'
                    self.machine.save()
        
        super().save(*args, **kwargs)
