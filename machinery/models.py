from django.db import models

# Create your models here.
class Machinery(models.Model):
    STATUS_CHOICES = [
        ('OK', 'OK'),
        ('Warning', 'Warning'),
        ('Fault', 'Fault'),
    ]

    machine_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='OK')
    priority = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.model})"
