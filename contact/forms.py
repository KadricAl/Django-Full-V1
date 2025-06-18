from django import forms

class ContactForm(forms.Form):
    email_or_phone = forms.CharField(label="Email or Phone", max_length=100, required=True, widget=forms.TextInput(attrs={
        'class': 'w-full p-2 border rounded',
        'placeholder': 'Enter your email or phone'
    }))
    title = forms.CharField(label="Title", max_length=200, required=True, widget=forms.TextInput(attrs={
        'class': 'w-full p-2 border rounded',
        'placeholder': 'Enter message title'
    }))
    message = forms.CharField(label="Message", widget=forms.Textarea(attrs={
        'class': 'w-full p-2 border rounded',
        'placeholder': 'Write your message here'
    }))

class RequestOfferForm(forms.Form):
    name = forms.CharField(label="Name", max_length=100, required=True, widget=forms.TextInput(attrs={
        'class': 'w-full p-2 border rounded',
        'placeholder': 'Your full name'
    }))
    email = forms.EmailField(label="Email", required=True, widget=forms.EmailInput(attrs={
        'class': 'w-full p-2 border rounded',
        'placeholder': 'Your email address'
    }))
    phone = forms.CharField(label="Phone", max_length=20, required=True, widget=forms.TextInput(attrs={
        'class': 'w-full p-2 border rounded',
        'placeholder': 'Your phone number'
    }))
    type = forms.ChoiceField(label="Type", choices=[
        ('product', 'Request Product Offer'),
        ('service', 'Request Service')
    ], widget=forms.Select(attrs={'class': 'w-full p-2 border rounded'}))
    description = forms.CharField(label="Short Description", widget=forms.Textarea(attrs={
        'class': 'w-full p-2 border rounded',
        'placeholder': 'Provide a short description'
    }))