from django.urls import path
from .views import *

urlpatterns = [
    path('add_receipt.html', add_receipt.as_view(), name="add_receipt"),
    path('list.html', list.as_view(), name='list_view'),
]
