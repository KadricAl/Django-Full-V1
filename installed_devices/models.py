from django.db import models
from django.utils import timezone
from datetime import timedelta
from devices.models import Device
from customer.models import Customer, Shop
from technician.models import TechnicianProfile

class InstalledDevice(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('installed', 'Installed'),
        ('deactivated', 'deactivated'),
    ]

    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    serial_number = models.CharField(max_length=100, unique=True)
    client = models.ForeignKey(Customer, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, default=1)
    technician = models.ForeignKey(TechnicianProfile, on_delete=models.SET_NULL, null=True)
    installation_date = models.DateField(default=timezone.localdate)
    warranty_expiry = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    last_yearly_service_done = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.warranty_expiry:
            self.warranty_expiry = self.installation_date + timedelta(days=365)
        super().save(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        if not self.last_yearly_service_done:
            self.last_yearly_service_done = self.installation_date
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.device.type} - {self.serial_number}"

