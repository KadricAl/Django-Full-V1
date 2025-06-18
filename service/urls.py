from django.urls import path
from . import views

urlpatterns = [
    path('', views.service_list, name='service_list'),  # Replace with your actual view
]
