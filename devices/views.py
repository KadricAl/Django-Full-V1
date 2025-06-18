from django.shortcuts import render

from django.shortcuts import render, get_object_or_404
from .models import Device
from django.core.paginator import Paginator
from django.db.models import Q

def product_list(request):
    query = request.GET.get('search')
    device_list = Device.objects.all()

    if query:
        device_list = device_list.filter(
            Q(type__icontains=query) | Q(description__icontains=query)
        )

    paginator = Paginator(device_list, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "devices/products.html", {
        "page_obj": page_obj,
        "search": query,
    })

def product_detail(request, pk):
    device = get_object_or_404(Device, pk=pk)
    return render(request, "devices/product_detail.html", {"device": device})

