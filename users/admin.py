from django.contrib import admin
from .models import User, Invoice, InvoiceItem, Product


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone_number']
    search_fields = ['name', 'phone_number']


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['user', 'invoice_number', 'total_amount', 'loading_amount', 'debit_amount', 'created']
    search_fields = ['user__name', 'invoice_number']


@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    model = InvoiceItem
    list_display = ['invoice', 'product', 'quantity', 'unit_price', 'price', 'created']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    search_fields = ['name']

