from django.urls import path
from .views import *

urlpatterns = [
    path('add_receipt.html', add_receipt.as_view(), name="add_receipt"),
    path('list.html', list.as_view(), name='list_view'),
    path('list_payee.html', payee_list.as_view(), name='payee'),
]
