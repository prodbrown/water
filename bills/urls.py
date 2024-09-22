from django.urls import path
from . import views
from .views import view_all_bills, approve_payment, payment_details

urlpatterns = [
    path('create/', views.create_bill, name='create_bill'),
    path('view/', views.view_bills, name='view_bills'),
    path('pay/<int:bill_id>/', views.pay_bill, name='pay_bill'),
    path('view_all_bills/', view_all_bills, name='view_all_bills'),
    path('approve_payment/<int:bill_id>/', approve_payment, name='approve_payment'),
    path('payment_details/<int:bill_id>/', payment_details, name='payment_details'),
    path('bills/reject/<int:bill_id>/', views.reject_bill, name='reject_bill'),
    path('bills/download-csv/', views.download_bills_csv, name='download_bills_csv') 
]
