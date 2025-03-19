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
        
class Collection(models.Model):
    collection_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class MachineryCollection(models.Model):
    mach_coll_id = models.AutoField(primary_key=True)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    machinery = models.ForeignKey(Machinery, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.machinery.name} in {self.collection.name}"
