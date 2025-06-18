from django.urls import path
from .views import technician_dashboard
from . import views

urlpatterns = [
    path('dashboard/', technician_dashboard, name='technician_dashboard'),
    path('dashboard/products/', views.technician_products, name='technician_products'),
    path('dashboard/products/add/', views.technician_add_product, name='technician_add_product'),
    path('dashboard/products/edit/<int:pk>/', views.technician_edit_product, name='technician_edit_product'),
    path('dashboard/products/delete/<int:pk>/', views.technician_delete_product, name='technician_delete_product'),
    path('clients/', views.technician_clients, name='technician_clients'),
    path('clients/add/', views.technician_add_client, name='technician_add_client'),
    path('clients/edit/<int:pk>/', views.edit_client, name='technician_edit_client'),
    path('clients/delete/<int:pk>/', views.delete_client, name='technician_delete_client'),
    path('clients/edit/create-shop/<int:client_id>/', views.create_shop, name='create_shop'),
    path('clients/edit/register/<int:client_id>/', views.register_client, name='register_client'),
    path('technician/all-devices/', views.technician_all_devices, name='technician_all_devices'),
    path('technician/add-device/', views.technician_add_device, name='technician_add_device'),
    path('devices/edit/<int:device_id>/', views.edit_installed_device, name='edit_installed_device'),
    path('devices/delete/<int:device_id>/', views.delete_installed_device, name='delete_installed_device'),
    path('requested-services/', views.technician_requested_services, name='technician_requested_services'),
    path('services/edit/<int:service_id>/', views.edit_service, name='technician_edit_service'),
    path('services/mark-completed/<int:service_id>/', views.technician_mark_completed, name='technician_mark_completed'),
    path('services/finished/', views.technician_finished_services, name='technician_finished_services'),
    path('services/finished/edit/<int:service_id>/', views.edit_finished_service, name='technician_edit_finished_service'),
    path('next-services/', views.technician_next_services, name='technician_next_services'),
    path('next-services/mark-completed/<int:device_id>/', views.mark_service_completed, name='technician_mark_service_completed'),
    path('next-services/cancel/<int:device_id>/', views.cancel_yearly_service, name='technician_cancel_service'),
]