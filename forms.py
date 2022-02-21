from django import forms
from .models import Receipt, SpendingAccount, BankAccount, Profile, StatementImport


class ReceiptForm(forms.ModelForm):
    def __init__(self, user_profile: Profile, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['from_account'].queryset = user_profile.bankaccount_set
        self.fields['to_account'].queryset = user_profile.spendingaccount_set

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


class StatementImportForm(forms.ModelForm):
    class Meta:
        model = StatementImport
        exclude = ['created_at']
