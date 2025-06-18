from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import date
from installed_devices.models import InstalledDevice
from customer.models import Customer, CustomerProfile, Shop
from service.models import Service
from django.db.models import Q
from django.utils import timezone
from .forms import ClientServiceRequestForm, RequestDeleteForm, RequestNewDeviceForm, ShopForm
from django.core.mail import send_mail
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
from io import BytesIO



def customer_list(request):
    return render(request, 'customer/customer_list.html')

@login_required
def client_dashboard(request):
    # Get the logged-in user's profile
    if hasattr(request.user, 'customerprofile'):
        customer_profile = request.user.customerprofile

        # Find the corresponding Customer record (based on email match)
        try:
            customer = Customer.objects.get(email=customer_profile.email)
        except Customer.DoesNotExist:
            return render(request, "customer/client_dashboard.html", {
                "error": "No customer data found."
            })

        # All shops for this customer
        shops = Shop.objects.filter(customer=customer)

        # All installed devices for this customer through their shops
        installed_devices = InstalledDevice.objects.filter(shop__in=shops)

        # Total devices
        total_devices = installed_devices.count()

        # Total shops
        total_shops = shops.count()

        # Current year
        current_year = date.today().year

        # Upcoming services: Devices whose last_yearly_service_done is not this year
        upcoming_services = installed_devices.exclude(
            last_yearly_service_done__year=current_year
        ).count()

        # Requested services with status 'Pending'
        requested_services = Service.objects.filter(
            installed_device__in=installed_devices,
            status='Pending'
        ).count()

        context = {
            'total_devices': total_devices,
            'total_shops': total_shops,
            'yearly_services': upcoming_services,
            'requested_services': requested_services
        }
        return render(request, "customer/client_dashboard.html", context)
    else:
        return redirect("home")
    
    
@login_required
def client_my_devices(request):
    if hasattr(request.user, 'customerprofile'):
        customer_profile = request.user.customerprofile

        try:
            customer = Customer.objects.get(email=customer_profile.email)
        except Customer.DoesNotExist:
            return render(request, "customer/my_devices.html", {
                "error": "Customer not found"
            })

        shops = Shop.objects.filter(customer=customer)
        installed_devices = InstalledDevice.objects.filter(shop__in=shops).select_related('device', 'shop')

        # Search filter (optional)
        search_query = request.GET.get('search', '')
        if search_query:
            installed_devices = installed_devices.filter(
                Q(serial_number__icontains=search_query)
            )

        context = {
            'devices': installed_devices,
            'search_query': search_query
        }

        return render(request, "customer/my_devices.html", context)

    return redirect("home")

@login_required
def client_request_service(request, device_id):
    device = get_object_or_404(InstalledDevice, id=device_id)

    if request.method == 'POST':
        form = ClientServiceRequestForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.service_type = 'Requested Service'
            service.request_date = timezone.now().date()
            service.status = 'Pending'
            service.installed_device = device
            service.save()
            return redirect('client_my_devices')
    else:
        form = ClientServiceRequestForm()

    return render(request, 'customer/request_service.html', {
        'device': device,
        'form': form
    })
    
    
@login_required
def request_device_delete(request, device_id):
    device = get_object_or_404(InstalledDevice, id=device_id)

    if request.method == 'POST':
        form = RequestDeleteForm(request.POST)
        if form.is_valid():
            reason = form.cleaned_data['reason']

            # Your business email (you can load from settings or hardcode here)
            business_email = 'yourbusiness@email.com'

            subject = f"Device Delete Request: {device.serial_number}"
            message = (
                f"A client has requested to delete the following device:\n\n"
                f"Serial Number: {device.serial_number}\n"
                f"Device Type: {device.device.type}\n"
                f"Installation Date: {device.installation_date}\n"
                f"Status: {device.status}\n\n"
                f"Reason:\n{reason}\n"
            )

            send_mail(
                subject,
                message,
                'almir.btscomp@gmail.com',  # From email
                [business_email],
                fail_silently=False,
            )

            messages.success(request, "Your delete request has been sent successfully.")
            return redirect('client_my_devices')
    else:
        form = RequestDeleteForm()

    return render(request, 'customer/request_delete.html', {
        'form': form,
        'device': device
    })
    
    
@login_required
def request_new_device_view(request):
    if not hasattr(request.user, 'customerprofile'):
        return redirect('home')

    customer_profile = request.user.customerprofile
    try:
        customer = Customer.objects.get(email=customer_profile.email)
    except Customer.DoesNotExist:
        return redirect('home')

    if request.method == 'POST':
        form = RequestNewDeviceForm(request.POST)
        form.fields['shop'].queryset = Shop.objects.filter(customer=customer)

        if form.is_valid():
            device_type = form.cleaned_data['device_type']
            expected_date = form.cleaned_data['expected_installation_date']
            shop = form.cleaned_data['shop']
            notes = form.cleaned_data['notes']

            # Send email
            send_mail(
                subject='[New Device Request] - {}'.format(device_type),
                message=(
                    f"Client: {customer.name}\n"
                    f"Email: {customer_profile.user.email}\n"
                    f"Device Type: {device_type}\n"
                    f"Expected Installation Date: {expected_date}\n"
                    f"Shop: {shop.name}, {shop.address}\n"
                    f"Notes: {notes or 'None'}"
                ),
                from_email='noreply@example.com',
                recipient_list=['almir.btscomp@gmail.com'],  # change this to your destination
                fail_silently=False
            )

            messages.success(request, "Your New device request has been sent successfully.")
            return redirect('client_my_devices')
        
    else:
        form = RequestNewDeviceForm()
        form.fields['shop'].queryset = Shop.objects.filter(customer=customer)

    return render(request, 'customer/request_new_device.html', {
        'form': form
    })
    

@login_required
def client_shops_view(request):
    if hasattr(request.user, 'customerprofile'):
        customer_profile = request.user.customerprofile

        try:
            customer = Customer.objects.get(email=customer_profile.email)
        except Customer.DoesNotExist:
            return redirect('client_dashboard')

        shops = Shop.objects.filter(customer=customer)

        return render(request, 'customer/client_shops.html', {
            'shops': shops
        })

    return redirect('home')

@login_required
def client_new_shop(request):
    if hasattr(request.user, 'customerprofile'):
        customer_profile = request.user.customerprofile
        try:
            customer = Customer.objects.get(email=customer_profile.email)
        except Customer.DoesNotExist:
            return redirect('client_dashboard')

        if request.method == 'POST':
            form = ShopForm(request.POST)
            if form.is_valid():
                shop = form.save(commit=False)
                shop.customer = customer
                shop.save()
                messages.success(request, "Shop created successfully.")
                return redirect('client_shops')
        else:
            form = ShopForm()

        return render(request, 'customer/client_shop_form.html', {'form': form, 'title': 'New Shop'})

    return redirect('home')


@login_required
def client_edit_shop(request, shop_id):
    if hasattr(request.user, 'customerprofile'):
        customer_profile = request.user.customerprofile
        try:
            customer = Customer.objects.get(email=customer_profile.email)
            shop = Shop.objects.get(id=shop_id, customer=customer)
        except (Customer.DoesNotExist, Shop.DoesNotExist):
            return redirect('client_shops')

        if request.method == 'POST':
            form = ShopForm(request.POST, instance=shop)
            if form.is_valid():
                form.save()
                messages.success(request, "Shop updated successfully.")
                return redirect('client_shops')
        else:
            form = ShopForm(instance=shop)

        return render(request, 'customer/client_shop_form.html', {'form': form, 'title': 'Edit Shop'})

    return redirect('home')


@login_required
def client_service_history(request):
    if not hasattr(request.user, 'customerprofile'):
        return redirect('home')

    customer_profile = request.user.customerprofile

    try:
        customer = Customer.objects.get(email=customer_profile.email)
    except Customer.DoesNotExist:
        return render(request, "customer/service_history.html", {"error": "Customer not found."})

    shops = Shop.objects.filter(customer=customer)
    installed_devices = InstalledDevice.objects.filter(shop__in=shops)

    services = Service.objects.filter(
        installed_device__in=installed_devices,
        status="Finished"
    ).select_related('installed_device', 'installed_device__device')

    # Filters
    serial_query = request.GET.get('serial', '')
    type_filter = request.GET.get('type', '')

    if serial_query:
        services = services.filter(installed_device__serial_number__icontains=serial_query)

    if type_filter:
        services = services.filter(service_type=type_filter)

    context = {
        'services': services,
        'serial_query': serial_query,
        'type_filter': type_filter,
    }
    return render(request, 'customer/service_history.html', context)


@login_required
def client_requested_services(request):
    if not hasattr(request.user, 'customerprofile'):
        return redirect('home')

    customer_profile = request.user.customerprofile

    try:
        customer = Customer.objects.get(email=customer_profile.email)
    except Customer.DoesNotExist:
        return render(request, "customer/requested_services.html", {"error": "Customer not found."})

    shops = Shop.objects.filter(customer=customer)
    installed_devices = InstalledDevice.objects.filter(shop__in=shops)

    services = Service.objects.filter(
        installed_device__in=installed_devices,
        status="Pending"
    ).select_related('installed_device', 'installed_device__device')

    context = {
        'services': services,
    }

    return render(request, "customer/requested_services.html", context)


from django.views.decorators.http import require_POST
from django.contrib import messages

@require_POST
@login_required
def client_cancel_service(request, service_id):
    try:
        service = Service.objects.get(id=service_id)

        # Ensure service belongs to this customer
        customer_profile = request.user.customerprofile
        customer = Customer.objects.get(email=customer_profile.email)
        if service.installed_device.shop.customer != customer:
            messages.error(request, "You are not authorized to cancel this request.")
            return redirect('client_requested_services')

        # Only allow cancelling if still pending
        if service.status == "Pending":
            service.status = "Cancelled"
            service.save()
            messages.success(request, "Service request cancelled.")
        else:
            messages.warning(request, "Only pending requests can be cancelled.")

    except Service.DoesNotExist:
        messages.error(request, "Service not found.")
    return redirect('client_requested_services')


@login_required
def client_next_services(request):
    if not hasattr(request.user, 'customerprofile'):
        return redirect('home')

    customer_profile = request.user.customerprofile
    try:
        customer = Customer.objects.get(email=customer_profile.email)
    except Customer.DoesNotExist:
        return redirect('home')

    today = date.today()
    current_year = today.year
    months = [today.month - 1, today.month, today.month + 1]

    # Normalize months
    months = [(m if m > 0 else 12) for m in months]
    months = [(m if m <= 12 else 1) for m in months]

    # Devices assigned to this customer
    shops = Shop.objects.filter(customer=customer)
    devices = InstalledDevice.objects.filter(
        shop__in=shops,
        status='installed'
    ).exclude(
        last_yearly_service_done__year=current_year
    )

    # Filter by due months
    due_devices = []
    for device in devices:
        try:
            service_due_date = date(current_year, device.installation_date.month, device.installation_date.day)
            if service_due_date.month in months:
                due_devices.append({
                    'device': device,
                    'due_date': service_due_date,
                })
        except ValueError:
            continue  # Skip invalid date (e.g., Feb 30)

    context = {
        'due_devices': due_devices,
    }
    return render(request, 'customer/next_services.html', context)



@login_required
def client_next_services_pdf(request):
    if not hasattr(request.user, 'customerprofile'):
        return redirect('home')

    customer_profile = request.user.customerprofile
    try:
        customer = Customer.objects.get(email=customer_profile.email)
    except Customer.DoesNotExist:
        return redirect('home')

    today = date.today()
    current_year = today.year
    months = [today.month - 1, today.month, today.month + 1]
    months = [(m if m > 0 else 12) for m in months]
    months = [(m if m <= 12 else 1) for m in months]

    shops = Shop.objects.filter(customer=customer)
    devices = InstalledDevice.objects.filter(
        shop__in=shops,
        status='installed'
    ).exclude(
        last_yearly_service_done__year=current_year
    )

    due_devices = []
    for device in devices:
        try:
            service_due_date = date(current_year, device.installation_date.month, device.installation_date.day)
            if service_due_date.month in months:
                due_devices.append({
                    'device': device,
                    'due_date': service_due_date,
                })
        except ValueError:
            continue

    html_string = render_to_string('customer/next_services_pdf.html', {
        'due_devices': due_devices,
        'customer': customer,
        'generated_on': date.today()
    })

    pdf_file = BytesIO()
    HTML(string=html_string).write_pdf(pdf_file)
    pdf_file.seek(0)

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="next_services.pdf"'
    return response
