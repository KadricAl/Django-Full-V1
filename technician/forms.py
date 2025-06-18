from django import forms
from devices.models import Device
from customer.models import Customer, Shop, CustomerProfile
from installed_devices.models import InstalledDevice
from service.models import Service

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['serial_number', 'type', 'description', 'price', 'picture']
        widgets = {
            'serial_number': forms.TextInput(attrs={'class': 'border p-2 w-full', 'placeholder': 'Enter product serial'}),
            'type': forms.TextInput(attrs={'class': 'border p-2 w-full', 'placeholder': 'Enter product type'}),
            'description': forms.Textarea(attrs={'class': 'border p-2 w-full', 'placeholder': 'Enter description'}),
            'price': forms.NumberInput(attrs={'class': 'border p-2 w-full', 'placeholder': 'Enter price'}),
            'picture': forms.FileInput(attrs={'class': 'border p-2 w-full img-file-pick', 'placeholder': 'Upload picture'}),
        }
        
        
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'border p-2 w-full', 'placeholder': 'Enter client name'}),
            'email': forms.EmailInput(attrs={'class': 'border p-2 w-full', 'placeholder': 'Enter email'}),
            'phone': forms.TextInput(attrs={'class': 'border p-2 w-full', 'placeholder': 'Enter phone number'}),
            'address': forms.TextInput(attrs={'class': 'border p-2 w-full', 'placeholder': 'Enter address'}),
        }


class InstalledDeviceForm(forms.ModelForm):
    class Meta:
        model = InstalledDevice
        fields = ['serial_number', 'device', 'client', 'shop', 'installation_date', 'status']
        widgets = {
            'serial_number': forms.TextInput(attrs={'class': 'border p-2 w-full', 'placeholder': 'Enter Serial Number'}),
            'device': forms.Select(attrs={'class': 'border p-2 w-full'}),
            'client': forms.Select(attrs={'class': 'border p-2 w-full'}),
            'shop': forms.Select(attrs={'class': 'border p-2 w-full'}),
            'installation_date': forms.DateInput(attrs={'class': 'border p-2 w-full', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'border p-2 w-full'}),
        }
        
        
class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['service_type', 'status', 'installed_device', 'client_description', 'tech_description', 'request_date', 'finish_date', 'price']
        widgets = {
            'service_type': forms.Select(attrs={'class': 'border p-2 w-full'}),
            'status': forms.Select(attrs={'class': 'border p-2 w-full'}),
            'installed_device': forms.Select(attrs={'class': 'border p-2 w-full'}),
            'client_description': forms.Textarea(attrs={'class': 'border p-2 w-full', 'rows': 3}),
            'tech_description': forms.Textarea(attrs={'class': 'border p-2 w-full', 'rows': 3}),
            'request_date': forms.DateInput(attrs={'class': 'border p-2 w-full', 'type': 'date'}),
            'finish_date': forms.DateInput(attrs={'class': 'border p-2 w-full', 'type': 'date'}),
            'price': forms.NumberInput(attrs={'class': 'border p-2 w-full'}),
        }
        
        
class FinishedServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['tech_description', 'price', 'finish_date', 'status']
        widgets = {
            'tech_description': forms.Textarea(attrs={'class': 'border p-2 w-full', 'placeholder': 'Enter service details'}),
            'price': forms.NumberInput(attrs={'class': 'border p-2 w-full', 'placeholder': 'Enter service price'}),
            'finish_date': forms.DateInput(attrs={'class': 'border p-2 w-full', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'border p-2 w-full'}),
        }
        


class MarkCompletedForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['finish_date', 'price', 'tech_description']
        widgets = {
            'finish_date': forms.DateInput(attrs={'class': 'border p-2 w-full', 'type': 'date'}),
            'price': forms.NumberInput(attrs={'class': 'border p-2 w-full', 'placeholder': 'Enter service price'}),
            'tech_description': forms.Textarea(attrs={'class': 'border p-2 w-full', 'placeholder': 'Enter service details'}),
        }


class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['name', 'address', 'phone', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'border p-2 w-full', 'placeholder': 'Enter client name'}),
            'email': forms.EmailInput(attrs={'class': 'border p-2 w-full', 'placeholder': 'Enter email'}),
            'phone': forms.TextInput(attrs={'class': 'border p-2 w-full', 'placeholder': 'Enter phone number'}),
            'address': forms.TextInput(attrs={'class': 'border p-2 w-full', 'placeholder': 'Enter address'}),
        }
        
        
class RegisterClientForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'border p-2 w-full rounded',
            'placeholder': 'Enter username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'border p-2 w-full rounded',
            'placeholder': 'Enter password'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'border p-2 w-full rounded',
            'placeholder': 'Enter email'
        })
    )

    class Meta:
        model = CustomerProfile
        fields = ['phone']
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'border p-2 w-full rounded',
                'placeholder': 'Enter phone number'
            }),
        }

    def __init__(self, *args, **kwargs):
        email_initial = kwargs.pop('email_initial', None)
        super().__init__(*args, **kwargs)
        if email_initial:
            self.fields['email'].initial = email_initial