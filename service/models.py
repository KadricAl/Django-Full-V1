from django.db import models

from customer.models import Shop
from devices.models import Device
from installed_devices.models import InstalledDevice
from django.utils import timezone

class Service(models.Model):
    SERVICE_TYPE_CHOICES = [
        ('Requested Service', 'Requested Service'),
        ('Yearly Service', 'Yearly Service'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Finished', 'Finished'),
        ('Cancelled', 'Cancelled'),
    ]

    service_type = models.CharField(max_length=50, choices=SERVICE_TYPE_CHOICES)
    request_date = models.DateField()
    finish_date = models.DateField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    installed_device = models.ForeignKey(InstalledDevice, on_delete=models.CASCADE, related_name='services')

    # Descriptions
    client_description = models.TextField(null=True, blank=True)
    tech_description = models.TextField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.status == 'Finished' and not self.finish_date:
            self.finish_date = timezone.now()
        super(Service, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.service_type} - {self.installed_device.serial_number} - {self.status}"

