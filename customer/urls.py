from django.urls import path
from . import views

urlpatterns = [
    path('', views.customer_list, name='customer_list'),
    path('client/dashboard/', views.client_dashboard, name='client_dashboard'),
    path('client/my-devices/', views.client_my_devices, name='client_my_devices'),
    path('client/request-service/<int:device_id>/', views.client_request_service, name='client_request_service'),
    path('client/request-delete/<int:device_id>/', views.request_device_delete, name='request_device_delete'),
    path('client/request-new-device/', views.request_new_device_view, name='request_new_device'),
    path('client/shops/', views.client_shops_view, name='client_shops'),
    path('client/shops/new/', views.client_new_shop, name='client_new_shop'),
    path('client/shops/edit/<int:shop_id>/', views.client_edit_shop, name='client_edit_shop'),
    path('client/service-history/', views.client_service_history, name='client_service_history'),
    path('client/requested-services/', views.client_requested_services, name='client_requested_services'),
    path('client/cancel-service/<int:service_id>/', views.client_cancel_service, name='client_cancel_service'),
    path('client/next-services/', views.client_next_services, name='client_next_services'),
    path('client/next-services/pdf/', views.client_next_services_pdf, name='client_next_services_pdf'),
]