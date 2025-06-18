from django.urls import path
from .views import index, about, login_page, login_view, custom_logout_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', index, name='home'),
    path('about/', about, name='about'),
    path('login/', login_page, name='login_page'),
    path('login/submit/', login_view, name='login_view'),
    path('logout/', custom_logout_view, name='logout'),
]