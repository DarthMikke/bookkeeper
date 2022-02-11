from django.urls import path
from .views import *

urlpatterns = [
    path('add.html', add_view),
]
