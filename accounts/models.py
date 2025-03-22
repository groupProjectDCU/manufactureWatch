from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):  #django's built-in user authentication - abstract user includes email & password
    ROLES = [
        ('TECHNICIAN', 'Technician'),
        ('REPAIR', 'Repair'),
        ('MANAGER', 'Manager'),
        ('VIEW-ONLY', 'View-only'),
    ]

    role = models.CharField(max_length=20, choices=ROLES, default='View-only')

    def __str__(self):
        return f"{self.username} - {self.role}"
