from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .forms import ContactForm, RequestOfferForm

def contact_view(request):
    contact_form = ContactForm()
    request_form = RequestOfferForm()

    if request.method == "POST":
        if "contact_submit" in request.POST:  # Contact Form
            contact_form = ContactForm(request.POST)
            if contact_form.is_valid():
                email_or_phone = contact_form.cleaned_data['email_or_phone']
                title = contact_form.cleaned_data['title']
                message = contact_form.cleaned_data['message']

                # Send email to business
                send_mail(
                    subject=f"New Contact Message: {title}",
                    message=f"From: {email_or_phone}\n\nMessage:\n{message}",
                    from_email="almir.btscomp@gmail.com",
                    recipient_list=["almir.btscomp@gmail.com"],
                )

                messages.success(request, "Message sent successfully!")
                return redirect('contact')

        elif "request_submit" in request.POST:  # Request Offer/Service Form
            request_form = RequestOfferForm(request.POST)
            if request_form.is_valid():
                name = request_form.cleaned_data['name']
                email = request_form.cleaned_data['email']
                phone = request_form.cleaned_data['phone']
                type_choice = request_form.cleaned_data['type']
                description = request_form.cleaned_data['description']

                # Send email confirmation to user
                send_mail(
                    subject="Your Request has been Received",
                    message=f"Dear {name},\n\nThank you for your {type_choice} request. We will contact you shortly!\n\nYour request details:\n{description}\n\nBest regards,\nYour Business",
                    from_email="almir.btscomp@gmail.com",
                    recipient_list=[email],
                )

                # Send email to business
                send_mail(
                    subject=f"New {type_choice} Request from {name}",
                    message=f"Email: {email}\nPhone: {phone}\n\nDescription:\n{description}",
                    from_email="almir.btscomp@gmail.com",
                    recipient_list=["almir.btscomp@gmail.com"],
                )

                messages.success(request, "Request sent successfully!")
                return redirect('contact')

    return render(request, "contact.html", {
        "contact_form": contact_form,
        "request_form": request_form
    })

# Create your views here.
