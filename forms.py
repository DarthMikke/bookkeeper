from django import forms
from .models import Receipt, SpendingAccount, BankAccount


class ReceiptForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = '__all__'


class PayeeForm(forms.ModelForm):
    class Meta:
        model = SpendingAccount
        fields = ['name']

class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ['name', 'balance']
