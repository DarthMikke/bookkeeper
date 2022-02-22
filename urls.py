from django.urls import path
from .views import *

urlpatterns = [
    path('list.html', List.as_view(), name='list_view'),
    path('month.html', MonthlyList.as_view(), name='monthly_list'),
    path('receipt_add.html', ReceiptAdd.as_view(), name="receipt_add"),
    path('receipt_edit.html', ReceiptAdd.as_view(), name="receipt_edit"),
    path('receipt_delete.html', ReceiptDelete.as_view(), name="receipt_delete"),
    path('payee_list.html', PayeeList.as_view(), name="payee_list"),
    path('payee_transactions.html', MonthlyList.as_view(), name='payee_transactions'),
    path('payee_add.html', PayeeAdd.as_view(), name='payee_add'),
    path('payee_delete.html', PayeeDelete.as_view(), name='payee_delete'),
    path('bank_account_list.html', BankAccountList.as_view(), name='bank_account_list'),
    path('bank_account_add.html', BankAccountAdd.as_view(), name='bank_account_add'),
    path('bank_account_edit.html', BankAccountAdd.as_view(), name='bank_account_edit'),
    path('bank_account_delete.html', BankAccountDelete.as_view(), name='bank_account_delete'),
    path('bank_account_transactions.html', MonthlyList.as_view(), name='bank_account_transactions'),
    path('bank_statement_import.html', StatementImportView.as_view(), name='bank_statement_import'),
    path('bank_statements/<import_id>.html', StatementView.as_view(), name='bank_statement'),
    path('bank_statements.html', StatementList.as_view(), name='bank_statements_list'),
]
