from django import forms
from .models import Receipt, Payee


class ReceiptForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = '__all__'


class PayeeForm(forms.ModelForm):
    class Meta:
        model = Payee
        fields = '__all__'