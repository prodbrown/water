from django import forms
from .models import Bill

class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['customer', 'month', 'year', 'units_used']

        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'month': forms.Select(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'units_used': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter units used'}),
        }
