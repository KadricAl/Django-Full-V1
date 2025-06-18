from django.db import models

class Device(models.Model):
    serial_number = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    picture = models.ImageField(upload_to='device_pictures/', blank=True, null=True)

    def __str__(self):
        return f"{self.type} ({self.serial_number})"
