from django import forms
from service.models import Service
from django.utils import timezone
from customer.models import Shop
from devices.models import Device

class ClientServiceRequestForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['service_type', 'request_date', 'client_description']

        widgets = {
            'service_type': forms.Select(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded'
            }),
            'request_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full p-2 border border-gray-300 rounded'
            }),
            'client_description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Describe the issue...',
                'class': 'w-full p-2 border border-gray-300 rounded',
            }),
        }

        labels = {
            'service_type': 'Service Type',
            'request_date': 'Request Date',
            'client_description': 'Describe the Issue',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set initial default values
        self.fields['service_type'].initial = 'Requested Service'
        self.fields['request_date'].initial = timezone.now().date()


class RequestDeleteForm(forms.Form):
    reason = forms.CharField(
        label="Reason for Deletion",
        widget=forms.Textarea(attrs={
            'rows': 4,
            'placeholder': 'Please explain why you want to delete this device...',
            'class': 'w-full p-2 border border-gray-300 rounded',
        }),
    )
    

class RequestNewDeviceForm(forms.Form):
    device_type = forms.ChoiceField(
        label="Device Type",
        choices=[],  # Will be set in __init__
        widget=forms.Select(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded'
        })
    )
    expected_installation_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'w-full p-2 border border-gray-300 rounded'
        })
    )
    shop = forms.ModelChoiceField(
        queryset=Shop.objects.none(),
        widget=forms.Select(attrs={'class': 'w-full p-2 border border-gray-300 rounded'})
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 4,
            'class': 'w-full p-2 border border-gray-300 rounded',
            'placeholder': 'Optional notes...'
        })
    )

    def __init__(self, *args, **kwargs):
        customer = kwargs.pop('customer', None)
        super().__init__(*args, **kwargs)

        # Set dynamic dropdown options
        device_types = Device.objects.values_list('type', flat=True).distinct()
        self.fields['device_type'].choices = [(dt, dt) for dt in device_types]

        # Filter shops if customer is passed
        if customer:
            self.fields['shop'].queryset = Shop.objects.filter(customer=customer)
            
            
            
class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['name', 'address', 'phone', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'address': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'phone': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-2 border rounded'}),
        }