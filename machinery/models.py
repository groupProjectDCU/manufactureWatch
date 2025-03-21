from django.db import models

# Create your models here.
class Machinery(models.Model):
    STATUS_CHOICES = [
        ('OK', 'OK'),
        ('Warning', 'Warning'),
        ('Fault', 'Fault'),
    ]

    machine_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='OK')
    priority = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.model})"
        
class Collection(models.Model):
    collection_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    machines = models.ManyToManyField(Machinery, through='MachineryCollection')

    def __str__(self):
        return self.name

class MachineryCollection(models.Model):
    mach_coll_id = models.BigAutoField(primary_key=True)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    machinery = models.ForeignKey(Machinery, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.machinery.name} in {self.collection.name}"

class MachineryAssignment(models.Model):
    assignment_id = models.BigAutoField(primary_key=True)
    is_active = models.BooleanField(default=True)
    assigned_at = models.DateTimeField(auto_now_add=True)
    machine = models.ForeignKey(Machinery, on_delete=models.CASCADE)
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assignments_created')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assignments_received')
    
    def __str__(self):
        return f"{self.machine.name} assigned to {self.assigned_to.get_full_name()}"

class Meta:
    unique_together = ('collection,' 'machinery')
    
class Meta:
        verbose_name_plural = "Machinery"


