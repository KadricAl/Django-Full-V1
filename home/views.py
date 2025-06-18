from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from technician.models import TechnicianProfile
from customer.models import CustomerProfile
from django.contrib.auth import logout

def index(request):
    return render(request, 'home/index.html')

def about(request):
    return render(request, 'home/about.html')

def login_page(request):
    return render(request, 'home/login.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        role = request.POST["role"]

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if role == "technician" and hasattr(user, "technicianprofile"):
                return redirect("technician_dashboard")
            elif role == "client" and hasattr(user, "customerprofile"):
                return redirect("client_dashboard")
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})

    return render(request, "login.html")


def custom_logout_view(request):
    logout(request)
    return redirect('home')