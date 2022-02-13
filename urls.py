from django.urls import path
from .views import *

urlpatterns = [
    path('add_receipt.html', add_receipt.as_view(), name="add_receipt"),
    path('edit_receipt.html', add_receipt.as_view(), name="edit_receipt"),
    path('delete_receipt.html', delete_receipt.as_view(), name="delete_receipt"),
    path('list.html', list.as_view(), name='list_view'),
    path('add_payee.html', add_payee.as_view(), name='add_payee'),
    path('list_payee.html', payee_list.as_view(), name='payee'),
    path('delete_payee.html', delete_payee.as_view(), name='delete_payee'),
    path('payee_transactions.html', payee_transactions.as_view(), name='payee_transactions')
]
