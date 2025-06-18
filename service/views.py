from django.shortcuts import render


def service_list(request):
    return render(request, 'service/service_list.html')  # Ensure the template exists

