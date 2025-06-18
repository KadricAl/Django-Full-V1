
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from .views import test_tailwind
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', test_tailwind, name='test_tailwind'),
    path('customers/', include('customer.urls')),
    path('services/', include('service.urls')),
    path('technicians/', include('technician.urls')),
    path('', include('home.urls')),
    path("contact/", include("contact.urls")),
    path("products/", include("devices.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
   
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
