from django.db import models
from model_utils.models import TimeStampedModel


class User(TimeStampedModel):
    name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True, unique=True)

    def __str__(self):
        return f"{self.id} | {self.phone_number}"


class Invoice(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='phone_number', null=True, blank=True)
    invoice_number = models.IntegerField(unique=True, null=True, blank=True)
    loading_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    debit_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.id}"


class Product(TimeStampedModel):
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.id}"


class InvoiceItem(TimeStampedModel):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items', null=True, blank=True) 
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items', null=True, blank=True,)
    quantity = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    unit = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.id}"


