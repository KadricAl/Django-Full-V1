from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import TechnicianProfile
from devices.models import Device
from installed_devices.models import InstalledDevice  # New app for installed devices
from customer.models import Customer, Shop, CustomerProfile
from service.models import Service
from .forms import DeviceForm, CustomerForm, InstalledDeviceForm, ServiceForm, FinishedServiceForm, MarkCompletedForm, ShopForm, RegisterClientForm
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User



@login_required
def technician_dashboard(request):
    if hasattr(request.user, 'technicianprofile'):
        technician = request.user.technicianprofile

        total_products = Device.objects.count()
        installed_devices = InstalledDevice.objects.count()
        total_clients = Customer.objects.count()
        awaiting_services = Service.objects.filter(status='Pending').count()  # adjust status value to match your model

        context = {
            'total_products': total_products,
            'installed_devices': installed_devices,
            'total_clients': total_clients,
            'awaiting_services': awaiting_services,
        }

        return render(request, 'technician/dashboard.html', context)
    else:
        return redirect('home')

@login_required
def technician_products(request):
    if not hasattr(request.user, 'technicianprofile'):
        return redirect('home')

    query = request.GET.get('search')
    products = Device.objects.all()

    if query:
        products = products.filter(
            Q(type__icontains=query) | Q(serial_number__icontains=query)
        )

    return render(request, 'technician/technician-products.html', {'products': products})
    
    
# Add new product
@login_required
def technician_add_product(request):
    if not hasattr(request.user, 'technicianprofile'):
        return redirect('home')

    if request.method == 'POST':
        form = DeviceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully!")
            return redirect('technician_products')
    else:
        form = DeviceForm()
    
    return render(request, 'technician/add_product.html', {'form': form})


# Edit product
@login_required
def technician_edit_product(request, pk):
    if not hasattr(request.user, 'technicianprofile'):
        return redirect('home')

    device = get_object_or_404(Device, pk=pk)
    if request.method == 'POST':
        form = DeviceForm(request.POST, request.FILES, instance=device)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully!")
            return redirect('technician_products')
    else:
        form = DeviceForm(instance=device)

    return render(request, 'technician/edit_product.html', {'form': form, 'device': device})


# Delete product
@login_required
def technician_delete_product(request, pk):
    if not hasattr(request.user, 'technicianprofile'):
        return redirect('home')

    device = get_object_or_404(Device, pk=pk)
    if request.method == 'POST':
        device.delete()
        messages.success(request, "Product deleted successfully!")
        return redirect('technician_products')

    return render(request, 'technician/delete_product_confirm.html', {'device': device})


@login_required
def technician_clients(request):
    if not hasattr(request.user, 'technicianprofile'):
        return redirect('home')

    search_query = request.GET.get('search', '')
    if search_query:
        clients = Customer.objects.filter(
            Q(name__icontains=search_query) | 
            Q(email__icontains=search_query) | 
            Q(phone__icontains=search_query)
        )
    else:
        clients = Customer.objects.all()
    
    client_data = []
    for client in clients:
        active_devices_count = InstalledDevice.objects.filter(client=client, status='Installed').count()
        client_data.append({
            'client': client,
            'active_devices_count': active_devices_count,
        })

    context = {
        'clients': client_data,
        'search_query': search_query,
    }
    return render(request, 'technician/technician-clients.html', context)

@login_required
def technician_add_client(request):
    if not hasattr(request.user, 'technicianprofile'):
        return redirect('home')

    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('technician_clients')
    else:
        form = CustomerForm()

    context = {
        'form': form,
    }
    return render(request, 'technician/add_client.html', context)


@login_required
def edit_client(request, pk):
    client = get_object_or_404(Customer, pk=pk)

    if request.method == "POST":
        form = CustomerForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('technician_clients')
    else:
        form = CustomerForm(instance=client)

    return render(request, 'technician/edit_client.html', {'form': form, 'client': client})

@login_required
def delete_client(request, pk):
    client = get_object_or_404(Customer, pk=pk)

    if request.method == "POST":
        client.delete()
        messages.success(request, "Client deleted successfully.")
        return redirect('technician_clients')

    return render(request, 'technician/delete_client.html', {'client': client})


@login_required
def technician_all_devices(request):
    if not hasattr(request.user, 'technicianprofile'):
        return redirect('home')

    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')

    devices = InstalledDevice.objects.all()

    # Search filter
    if search_query:
        devices = devices.filter(
            Q(serial_number__icontains=search_query) |
            Q(client__name__icontains=search_query)
        )
    
    # Status filter
    if status_filter:
        devices = devices.filter(status=status_filter)

    context = {
        'devices': devices,
        'search_query': search_query,
        'status_filter': status_filter,
    }
    return render(request, 'technician/technician_all_devices.html', context)


@login_required
def technician_add_device(request):
    if not hasattr(request.user, 'technicianprofile'):
        return redirect('home')

    if request.method == "POST":
        form = InstalledDeviceForm(request.POST)
        if form.is_valid():
            device = form.save(commit=False)

            # If no shop is selected, assign to default
            if not device.shop:
                device.shop = Shop.objects.get(name='Default Shop')
                
            device.save()
            return redirect('technician_all_devices')
    else:
        form = InstalledDeviceForm()

    context = {
        'form': form,
    }
    return render(request, 'technician/add_device.html', context)


@login_required
def technician_requested_services(request):
    if not hasattr(request.user, 'technicianprofile'):
        return redirect('home')

    search_query = request.GET.get('search', '')

    # Filter services by status and search query
    services = Service.objects.filter(status='Pending')

    if search_query:
        services = services.filter(
            Q(device__serial_number__icontains=search_query) |
            Q(device__client__name__icontains=search_query)
        )

    context = {
        'services': services,
    }
    return render(request, 'technician/requested_services.html', context)


@login_required
def edit_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)

    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            print('heloooooooouuuuuuuu')
            return redirect('technician_requested_services')
    else:
        form = ServiceForm(instance=service)

    context = {
        'form': form,
        'service': service,
    }

    return render(request, 'technician/edit_service.html', context)


@login_required
def technician_mark_completed(request, service_id):
    if not hasattr(request.user, 'technicianprofile'):
        return redirect('home')

    service = get_object_or_404(Service, id=service_id)

    # Update service status
    service.status = 'Finished'
    service.finish_date = timezone.now()
    service.save()

    messages.success(request, "Service marked as completed.")
    return redirect('technician_requested_services')


@login_required
def technician_finished_services(request):
    if not hasattr(request.user, 'technicianprofile'):
        return redirect('home')

    # Fetch the last 50 finished services ordered by finish_date descending
    finished_services = Service.objects.filter(status='Finished').order_by('-finish_date')[:50]

    context = {
        'services': finished_services,
    }
    return render(request, 'technician/finished_services.html', context)


@login_required
def edit_finished_service(request, service_id):
    if not hasattr(request.user, 'technicianprofile'):
        return redirect('home')

    # Allow editing regardless of status
    service = get_object_or_404(Service, id=service_id)

    if request.method == 'POST':
        form = FinishedServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, "Service updated successfully.")
            return redirect('technician_finished_services')  # Go back to list of finished services
    else:
        form = FinishedServiceForm(instance=service)

    context = {
        'form': form,
        'service': service,
    }
    return render(request, 'technician/edit_finished_service.html', context)


@login_required
def edit_installed_device(request, device_id):
    device = get_object_or_404(InstalledDevice, id=device_id)

    if request.method == 'POST':
        form = InstalledDeviceForm(request.POST, request.FILES, instance=device)
        if form.is_valid():
            form.save()
            messages.success(request, "Device updated successfully.")
            return redirect('technician_all_devices')
    else:
        form = InstalledDeviceForm(instance=device)

    return render(request, 'technician/edit_device.html', {'form': form, 'device': device})


@login_required
def delete_installed_device(request, device_id):
    device = get_object_or_404(InstalledDevice, id=device_id)

    if request.method == 'POST':
        device.delete()
        messages.success(request, "Device deleted successfully.")
        return redirect('technician_all_devices')

    return render(request, 'technician/delete_device.html', {'device': device})


from datetime import date, timedelta
from django.db.models import Q
from django.utils.timezone import now

@login_required
def technician_next_services(request):
    if not hasattr(request.user, 'technicianprofile'):
        return redirect('home')

    today = date.today()
    current_year = today.year
    months = [today.month - 1, today.month, today.month + 1]

    # Normalize months (handle Jan/Dec rollover)
    months = [(m if m > 0 else 12) for m in months]
    months = [(m if m <= 12 else 1) for m in months]

    # Devices eligible for reminder
    devices = InstalledDevice.objects.filter(
        status='installed'
    ).exclude(
        last_yearly_service_done__year=current_year  # Exclude already serviced this year
    )

    # Filter those with service due date in target months
    due_devices = []
    for device in devices:
        service_due_date = date(current_year, device.installation_date.month, device.installation_date.day)

        if service_due_date.month in months:
            due_devices.append({
                'device': device,
                'due_date': service_due_date,
            })

    context = {
        'due_devices': due_devices,
    }
    print(due_devices)
    return render(request, 'technician/next_services.html', context)


@login_required
def mark_service_completed(request, device_id):
    device = get_object_or_404(InstalledDevice, id=device_id, status='installed')

    if request.method == 'POST':
        form = MarkCompletedForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)

            # Auto-set fields
            install_date = device.installation_date
            current_year = timezone.now().year
            yearly_request_date = install_date.replace(year=current_year)

            service.installed_device = device  # ✅ This line assigns the required FK!
            service.technician = request.user.technicianprofile
            service.status = "Finished"
            service.service_type = "Yearly Service"
            service.request_date = yearly_request_date
            service.save()

            device.last_yearly_service_done = timezone.now().date()
            device.save()

            messages.success(request, "Service marked as completed.")
            return redirect('technician_next_services')
    else:
        form = MarkCompletedForm()

    return render(request, 'technician/mark_completed.html', {
        'form': form,
        'device': device
    })


@login_required
def cancel_yearly_service(request, device_id):
    device = get_object_or_404(InstalledDevice, id=device_id, status='installed')

    if request.method == 'POST':
        device.last_yearly_service = False
        device.save()
        messages.success(request, "Service marked as not completed for this year.")
        return redirect('technician_next_services')

    return render(request, 'technician/cancel_yearly_service.html', {'device': device})


@login_required
def create_shop(request, client_id):
    client = get_object_or_404(Customer, id=client_id)

    if request.method == 'POST':
        form = ShopForm(request.POST)
        if form.is_valid():
            shop = form.save(commit=False)
            shop.customer = client 
            shop.save()
            messages.success(request, f"Shop created for client {client.name}.")
            return redirect('technician_edit_client', pk=client.id)
    else:
        form = ShopForm()

    return render(request, 'technician/create_shop.html', {
        'form': form,
        'client': client
    })



@login_required
def register_client(request, client_id):
    client = get_object_or_404(Customer, id=client_id)

    if request.method == 'POST':
        form = RegisterClientForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']

            # Create the user
            user = User.objects.create_user(username=username, email=email, password=password)

            # Create the profile and link it to the User
            CustomerProfile.objects.create(
                user=user,
                phone=phone,
                email=email,
                is_customer=True
            )

            # Link user to Customer model
            client.user = user
            client.save()

            # Send login credentials
            send_mail(
                subject='Your Client Dashboard Login',
                message=f"Hello {username},\n\nYour account has been created.\nLogin at: https://yourdomain.com/login/\nUsername: {username}\nPassword: {password}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )

            messages.success(request, f"Client '{username}' registered and credentials sent.")
            return redirect('technician_edit_client', pk=client.id)

    else:
        form = RegisterClientForm(email_initial=client.email)  # Pass client email here

    return render(request, 'technician/register_client.html', {
        'form': form,
        'client': client
    })

