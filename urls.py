from django.urls import path
from .views import *

urlpatterns = [
    path('list.html', list.as_view(), name='list_view'),
    path('receipt_add.html', receipt_add.as_view(), name="receipt_add"),
    path('receipt_edit.html', receipt_add.as_view(), name="receipt_edit"),
    path('receipt_delete.html', receipt_delete.as_view(), name="receipt_delete"),
    path('payee_list.html', payee_list.as_view(), name="payee_list"),
    path('payee_transactions.html', payee_transactions.as_view(), name='payee_transactions'),
    path('payee_add.html', payee_add.as_view(), name='payee_add'),
    path('payee_delete.html', payee_delete.as_view(), name='payee_delete'),
    path('bank_account_list.html', bank_account_list.as_view(), name='bank_account_list'),
    path('bank_account_add.html', bank_account_add.as_view(), name='bank_account_add'),
    path('bank_account_edit.html', bank_account_add.as_view(), name='bank_account_edit'),
    path('bank_account_delete.html', bank_account_delete.as_view(), name='bank_account_delete'),
    path('bank_account_transactions.html', bank_account_add.as_view(), name='bank_account_transactions'),
]
