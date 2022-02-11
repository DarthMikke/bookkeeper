from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Profile)
admin.site.register(BankAccount)
admin.site.register(SpendingAccount)
admin.site.register(Receipt)
