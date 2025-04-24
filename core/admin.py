from django.contrib import admin
from .models import Category, PaymentMethod, Account, Expense, Cheque

admin.site.register(Category)
admin.site.register(PaymentMethod)
admin.site.register(Account)
admin.site.register(Expense)
admin.site.register(Cheque)
