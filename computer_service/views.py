from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import ServiceRequest, Invoice, Part, ServiceTechnician, Customer
from .forms import ServiceRequestForm, InvoiceForm #, PartForm, ServiceTechnicianForm, CustomerForm
from django.urls import reverse

# Create your views here.
def index(request):
    return HttpResponse("Welcome in Computer service")

def service_request_list(request):
    service_requests = ServiceRequest.objects.all()
    return render(request, 'computerserviceapp/service_request_list.html', {'service_requests': service_requests})

def service_request_detail(request, pk):
    service_request = get_object_or_404(ServiceRequest, pk=pk)
    return render(request, 'computerserviceapp/service_request_detail.html', {'service_request': service_request})

def service_request_create(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            service_request = form.save()
            return redirect('service_request_detail', pk=service_request.pk)
    else:
        form = ServiceRequestForm()
    return render(request, 'computerserviceapp/service_request_form.html', {'form': form})

def service_request_edit(request, pk):
    service_request = get_object_or_404(ServiceRequest, pk=pk)
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST, instance=service_request)
        if form.is_valid():
            service_request = form.save()
            return redirect('service_request_detail', pk=service_request.pk)
    else:
        form = ServiceRequestForm(instance=service_request)
    return render(request, 'computerserviceapp/service_request_form.html', {'form': form})

def service_request_delete(request, pk):
    service_request = get_object_or_404(ServiceRequest, pk=pk)
    if request.method == 'POST':
        service_request.delete()
        return redirect('service_request_list')
    return render(request, 'computerserviceapp/service_request_confirm_delete.html', {'service_request': service_request})

##TO DO##
# Similar views for Invoice, Part, ServiceTechnician, and Customer...

