from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Bill, Payment
from .forms import BillForm
from django.contrib import messages
from django.http import HttpResponse
import csv

# Error handling function
def handle_error(request, error_message):
    return render(request, 'error.html', {'error_message': error_message})

# CREATE BILL
@login_required
def create_bill(request):
    if request.user.is_serviceprovider:
        if request.method == 'POST':
            form = BillForm(request.POST)
            if form.is_valid():
                bill = form.save(commit=False)
                bill.service_provider = request.user
                bill.save()
                messages.success(request, 'Bill created successfully.')
                return redirect('view_all_bills')
            else:
                messages.error(request, 'Error creating bill. Please check your input.')
        else:
            form = BillForm()
        return render(request, 'bills/create_bill.html', {'form': form})
    else:
        return redirect('dashboard')

# VIEW BILL
@login_required
def view_bills(request):
    if request.user.is_customer:
        bills = Bill.objects.filter(customer=request.user)
        
        # Filter by status
        status_filter = request.GET.get('status')
        if status_filter:
            bills = bills.filter(status=status_filter)

        # Total counts
        total_paid = bills.filter(status='PAID').count()
        total_pending = bills.filter(status='PENDING').count()
        total_not_paid = bills.filter(status='NOT PAID').count()
        total_rejected = bills.filter(status='REJECTED').count()

        return render(request, 'bills/view_bills.html', {
            'bills': bills,
            'total_paid': total_paid,
            'total_pending': total_pending,
            'total_not_paid': total_not_paid,
            'total_rejected': total_rejected,
        })
    else:
        return redirect('dashboard')

# PAY BILL
@login_required
def pay_bill(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id, customer=request.user)
    if request.method == 'POST':
        try:
            bill.payment_verification_message = request.POST.get('verification_message')
            bill.payment_verification_screenshot = request.FILES.get('screenshot')
            bill.status = 'PENDING'  # Set status to PENDING until verified
            bill.save()
            messages.success(request, 'Payment details submitted successfully.')
            return redirect('view_bills')
        except Exception as e:
            return handle_error(request, str(e))
    return render(request, 'bills/pay_bill.html', {'bill': bill})

# VIEW ALL BILLS
@login_required
@user_passes_test(lambda u: u.is_superuser)
def view_all_bills(request):
    status_filter = request.GET.get('status')
    if status_filter:
        bills = Bill.objects.filter(status=status_filter)
    else:
        bills = Bill.objects.all()

    total_bills = bills.count()
    total_paid = bills.filter(status='PAID').count()
    total_pending = bills.filter(status='PENDING').count()
    total_not_paid = bills.filter(status='NOT PAID').count()
    total_rejected = bills.filter(status='REJECTED').count()

    context = {
        'bills': bills,
        'total_bills': total_bills,
        'total_paid': total_paid,
        'total_pending': total_pending,
        'total_not_paid': total_not_paid,
        'total_rejected': total_rejected,
        'status_filter': status_filter
    }
    return render(request, 'bills/view_all_bills.html', context)

# APPROVE PAYMENTS
@login_required
@user_passes_test(lambda u: u.is_serviceprovider)
def approve_payment(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id, service_provider=request.user)
    if request.method == 'POST':
        try:
            bill.status = 'PAID'
            Payment.objects.create(bill=bill, paid_amount=bill.total_amount)
            messages.success(request, 'Payment approved successfully.')
            bill.save()
            return redirect('view_all_bills')
        except Exception as e:
            return handle_error(request, str(e))
    return render(request, 'bills/approve_payment.html', {'bill': bill})

# PAYMENT DETAILS
@login_required
def payment_details(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    payment = Payment.objects.filter(bill=bill).first()
    
    context = {
        'bill': bill,
        'payment': payment
    }
    return render(request, 'bills/payment_details.html', context)

# REJECT BILLS
@login_required
@user_passes_test(lambda u: u.is_serviceprovider)
def reject_bill(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id, service_provider=request.user)
    
    if request.method == 'POST':
        try:
            bill.status = 'REJECTED'
            bill.payment_verification_message = ''
            bill.payment_verification_screenshot = None
            bill.save()
            messages.success(request, 'Bill rejected successfully.')
            return redirect('view_all_bills')
        except Exception as e:
            return handle_error(request, str(e))

    return render(request, 'bills/reject_bill.html', {'bill': bill})

# DOWNLOAD BILLS
@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_serviceprovider)
def download_bills_csv(request):
    try:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="bills.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Customer', 'Month', 'Year', 'Units Used', 'Total Amount', 'Status', 'Control Number'])

        status_filter = request.GET.get('status')
        if status_filter:
            bills = Bill.objects.filter(status=status_filter)
        else:
            bills = Bill.objects.all()

        for bill in bills:
            writer.writerow([
                bill.customer.email, 
                bill.month, 
                bill.year, 
                bill.units_used, 
                bill.total_amount, 
                bill.status, 
                bill.control_number
            ])

        return response
    except Exception as e:
        return handle_error(request, str(e))
