from django.db import models

from django.db import models
from django.contrib.auth.models import User

class TechnicianProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=100, blank=True)
    is_technician = models.BooleanField(default=True)
    department = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} - {self.department}"

