from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):  #django's built-in user authentication - abstract user includes email & password
    user_id = models.BigAutoField(primary_key=True) #explicit primary key
    first_name = models.CharField(max_length=255, unique=True)    #can change if necessary
    last_name = models.CharField(max_length=255, unique=True)  #ditto
    
    ROLES = [
        ('Technician', 'Technician'),
        ('Repair', 'Repair'),
        ('Manager', 'Manager'),
        ('View-only', 'View-only'),
    ]

    role = models.CharField(max_length=20, choices=ROLES, default='View-only')

    def __str__(self):
        return f"{self.username} - {self.role}"
