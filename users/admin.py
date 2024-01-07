from django.contrib import admin
from .models import User, Invoice, InvoiceItem, Product

# Register User model
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone_number']
    search_fields = ['name', 'phone_number']

# Register Invoice model
@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['user', 'invoice_number', 'total_amount', 'loading_amount', 'debit_amount']
    search_fields = ['user__name', 'invoice_number']


# Define inline form for InvoiceItem
@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    model = InvoiceItem


# Register Product model
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

