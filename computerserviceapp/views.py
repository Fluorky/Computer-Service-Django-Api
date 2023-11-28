from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import ServiceRequest, Invoice, Part, ServiceTechnician, Customer
from .forms import ServiceRequestForm, InvoiceForm , PartForm, ServiceTechnicianForm, CustomerForm
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

## TO DO ##
# htmls 
# css

#def index(request):
    #return HttpResponse("Welcome in Computer service")

class IndexView(View):
    def get(self, request):
        return render(request, 'computerserviceapp/index.html') 



class ServiceRequestListView(View):
    def get(self, request):
        service_requests = ServiceRequest.objects.all()
        return render(request, 'computerserviceapp/lists/service_request_list.html', {'service_requests': service_requests})


class ServiceRequestDetailView(View):
    def get(self, request, pk):
        service_request = get_object_or_404(ServiceRequest, pk=pk)
        return render(request, 'computerserviceapp/details/service_request_detail.html', {'service_request': service_request})


class ServiceRequestCreateView(View):
    def get(self, request):
        form = ServiceRequestForm()
        return render(request, 'computerserviceapp/forms/service_request_form.html', {'form': form})

    def post(self, request):
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            service_request = form.save()
            return redirect('service_request_detail', pk=service_request.pk)
        return render(request, 'computerserviceapp/forms/service_request_form.html', {'form': form})


class ServiceRequestUpdateView(View):
    def get(self, request, pk):
        service_request = get_object_or_404(ServiceRequest, pk=pk)
        form = ServiceRequestForm(instance=service_request)
        return render(request, 'computerserviceapp/forms/service_request_form.html', {'form': form})

    def post(self, request, pk):
        service_request = get_object_or_404(ServiceRequest, pk=pk)
        form = ServiceRequestForm(request.POST, instance=service_request)
        if form.is_valid():
            service_request = form.save()
            return redirect('service_request_detail', pk=service_request.pk)
        return render(request, 'computerserviceapp/forms/service_request_form.html', {'form': form})


class ServiceRequestDeleteView(View):
    def get(self, request, pk):
        service_request = get_object_or_404(ServiceRequest, pk=pk)
        return render(request, 'computerserviceapp/delete/service_request_confirm_delete.html', {'service_request': service_request})

    def post(self, request, pk):
        service_request = get_object_or_404(ServiceRequest, pk=pk)
        service_request.delete()
        return redirect('service_request_list')

"""class ServiceRequestDeleteView(DeleteView):
    model = ServiceRequest
    template_name = 'computerserviceapp/delete/service_request_confirm_delete.html'
    success_url = reverse_lazy('service_request_list')
"""

"""def service_request_list(request):
    service_requests = ServiceRequest.objects.all()
    return render(request, 'computerserviceapp/lists/service_request_list.html', {'service_requests': service_requests})

def service_request_detail(request, pk):
    service_request = get_object_or_404(ServiceRequest, pk=pk)
    return render(request, 'computerserviceapp/details/service_request_detail.html', {'service_request': service_request})

def service_request_create(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            service_request = form.save()
            return redirect('service_request_detail', pk=service_request.pk)
    else:
        form = ServiceRequestForm()
    return render(request, 'computerserviceapp/forms/service_request_form.html', {'form': form})

def service_request_edit(request, pk):
    service_request = get_object_or_404(ServiceRequest, pk=pk)
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST, instance=service_request)
        if form.is_valid():
            service_request = form.save()
            return redirect('service_request_detail', pk=service_request.pk)
    else:
        form = ServiceRequestForm(instance=service_request)
    return render(request, 'computerserviceapp/forms/service_request_form.html', {'form': form})
"""
"""def service_request_delete(request, pk):
    service_request = get_object_or_404(ServiceRequest, pk=pk)
    if request.method == 'POST':
        service_request.delete()
        return redirect('service_request_list')
    return render(request, 'computerserviceapp/delete/service_request_confirm_delete.html', {'service_request': service_request})"""


def invoice_list(request):
    invoices = Invoice.objects.all()
    return render(request, 'computerserviceapp/lists/invoice_list.html', {'invoices': invoices})


def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    return render(request, 'computerserviceapp/details/invoice_detail.html', {'invoice': invoice})

def invoice_create(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save()
            return redirect('invoice_detail', pk=invoice.pk)
    else:
        form = InvoiceForm()
    return render(request, 'computerserviceapp/forms/invoice_form.html', {'form': form})

def invoice_edit(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            invoice = form.save()
            return redirect('invoice_detail', pk=invoice.pk)
    else:
        form = InvoiceForm(instance=invoice)
    return render(request, 'computerserviceapp/forms/invoice_form.html', {'form': form})

def invoice_delete(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == 'POST':
        invoice.delete()
        return redirect('invoice_list')
    return render(request, 'computerserviceapp/delete/invoice_confirm_delete.html', {'invoice': invoice})


def part_list(request):
    parts = Part.objects.all()
    return render(request, 'computerserviceapp/lists/part_list.html', {'parts': parts})

def part_detail(request, pk):
    part = get_object_or_404(Part, pk=pk)
    return render(request, 'computerserviceapp/details/part_detail.html', {'part': part})

def part_create(request):
    if request.method == 'POST':
        form = PartForm(request.POST)
        if form.is_valid():
            part = form.save()
            return redirect('part_detail', pk=part.pk)
    else:
        form = PartForm()
    return render(request, 'computerserviceapp/forms/part_form.html', {'form': form})

def part_edit(request, pk):
    part = get_object_or_404(Part, pk=pk)
    if request.method == 'POST':
        form = PartForm(request.POST, instance=part)
        if form.is_valid():
            part = form.save()
            return redirect('part_detail', pk=part.pk)
    else:
        form = PartForm(instance=part)
    return render(request, 'computerserviceapp/forms/part_form.html', {'form': form})

def part_delete(request, pk):
    part = get_object_or_404(Part, pk=pk)
    if request.method == 'POST':
        part.delete()
        return redirect('part_list')
    return render(request, 'computerserviceapp/delete/part_confirm_delete.html', {'part': part})


def service_technician_list(request):
    service_technicians = ServiceTechnician.objects.all()
    return render(request, 'computerserviceapp/lists/service_technician_list.html', {'service_technicians': service_technicians})

def service_technician_detail(request, pk):
    service_technician = get_object_or_404(ServiceTechnician, pk=pk)
    return render(request, 'computerserviceapp/details/service_technician_detail.html', {'service_technician': service_technician})

def service_technician_create(request):
    if request.method == 'POST':
        form = ServiceTechnicianForm(request.POST)
        if form.is_valid():
            service_technician = form.save()
            return redirect('service_technician_detail', pk=service_technician.pk)
    else:
        form = ServiceTechnicianForm()
    return render(request, 'computerserviceapp/forms/service_technician_form.html', {'form': form})

def service_technician_edit(request, pk):
    service_technician = get_object_or_404(ServiceTechnician, pk=pk)
    if request.method == 'POST':
        form = ServiceTechnicianForm(request.POST, instance=service_technician)
        if form.is_valid():
            service_technician = form.save()
            return redirect('service_technician_detail', pk=service_technician.pk)
    else:
        form = ServiceTechnicianForm(instance=service_technician)
    return render(request, 'computerserviceapp/forms/service_technician_form.html', {'form': form})

def service_technician_delete(request, pk):
    service_technician = get_object_or_404(ServiceTechnician, pk=pk)
    if request.method == 'POST':
        service_technician.delete()
        return redirect('service_technician_list')
    return render(request, 'computerserviceapp/delete/service_technician_confirm_delete.html', {'service_technician': service_technician})


def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'computerserviceapp/lists/customer_list.html', {'customers': customers})

def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, 'computerserviceapp/details/customer_detail.html', {'customer': customer})

def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            return redirect('customer_detail', pk=customer.pk)
    else:
        form = CustomerForm()
    return render(request, 'computerserviceapp/forms/customer_form.html', {'form': form})

def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            customer = form.save()
            return redirect('customer_detail', pk=customer.pk)
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'computerserviceapp/forms/customer_form.html', {'form': form})

def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('customer_list')
    return render(request, 'computerserviceapp/delete/customer_confirm_delete.html', {'customer': customer})
##TO DO##
