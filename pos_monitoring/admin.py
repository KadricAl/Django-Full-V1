from django.contrib import admin
from customer.models import Customer, Shop
from service.models import Service
from technician.models import TechnicianProfile

admin.site.register(Customer)
admin.site.register(Shop)
admin.site.register(Service)
admin.site.register(TechnicianProfile)