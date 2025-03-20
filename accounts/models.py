from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):  #django's built-in user authentication
    ROLES = [
        ('Technician', 'Technician'),
        ('Repair', 'Repair'),
        ('Manager', 'Manager'),
        ('View-only', 'View-only'),
    ]

    role = models.CharField(max_length=20, choices=ROLES, default='View-only')

    def __str__(self):
        return f"{self.username} - {self.role}"
