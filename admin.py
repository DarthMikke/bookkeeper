from django.contrib import admin
from .models import *


class StatementAdmin(admin.ModelAdmin):
    list_display = ('account', 'created_at', 'should_delete')


# Register your models here.
admin.site.register(Profile)
admin.site.register(BankAccount)
admin.site.register(SpendingAccount)
admin.site.register(Receipt)
admin.site.register(StatementImport, StatementAdmin)
