from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = [
        ('MANAGER', 'Manager'),
        ('TECHNICIAN', 'Technician'),
        ('REPAIR', 'Repair'),
        ('VIEW_ONLY', 'View-only'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='VIEW_ONLY')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"


class FaultCase:
    pass