import pytz
from decimal import Decimal

from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

from .models import User, Invoice, InvoiceItem, Product
from django.utils import timezone



def homepage_view(request):
    return render(request, 'homepage.html')


def create_user(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone_number = request.POST.get('phone')

        existing_user = User.objects.filter(phone_number=phone_number).first()

        if existing_user:
            existing_invoice = Invoice.objects.filter(invoice_number__isnull=False).last()
            if not existing_invoice:
                new_invoice = Invoice.objects.create(user=existing_user)
                invoice_id = new_invoice.id
            else:
                invoice_id = existing_invoice.invoice_number + 1
            return redirect('invoice', invoice_id, existing_user.id)

        new_user = User.objects.create(name=name, phone_number=phone_number)
        invoice = Invoice.objects.create(user=new_user)

        return redirect('invoice',  invoice.id, new_user.id)

    return render(request, 'homepage.html')


def generate_invoice(request, invoice_id, user_id):
    user = get_object_or_404(User, id=user_id)
    existing_invoice = Invoice.objects.filter(user=user, invoice_number__isnull=False).last()

    if existing_invoice and existing_invoice.debit_amount > 0:
        previous_debit_amount = existing_invoice.debit_amount
    else:
        previous_debit_amount = 0

    products = Product.objects.all()
    karachi_timezone = pytz.timezone('Asia/Karachi')
    utc_now = timezone.now()
    karachi_time = utc_now.astimezone(karachi_timezone)

    response = render(
        request,
        'index.html', {
            'user': user,
            'invoice_id': invoice_id,
            'products': products,
            'current_date': karachi_time.date(),
            'previous_debit_amount': previous_debit_amount
        }
    )
    
    return response


def save_data(request):
    name = request.POST.get('name')
    phone = request.POST.get('phone')
    invoice_id = request.POST.get('invoice_id')
    loading_amount = request.POST.get('loading_amount')
    debit_amount = request.POST.get('debit_amount')

    unit_price_list = request.POST.getlist('unit_price')
    quantity_list = request.POST.getlist('quantity')
    product_list = request.POST.getlist('product')
    unit_list = request.POST.getlist('unit')

    if loading_amount == '':
        loading_amount = 0
    if debit_amount == '':
        debit_amount = 0

    total_amount = 0
    user = get_object_or_404(User, phone_number=phone)
    user_invoice = Invoice.objects.filter(invoice_number__isnull=True).last()
    if not user_invoice:
        user_invoice = Invoice.objects.create(user=user)

    for unit_price, product_id, quantity, unit in zip(
        unit_price_list, product_list, quantity_list, unit_list
    ):
        unit_price = float(unit_price)
        product_id = int(product_id)
        quantity = int(quantity)

        price = unit_price * quantity
        total_amount += price

        InvoiceItem.objects.create(
            invoice=user_invoice,
            product_id=product_id,
            quantity=quantity,
            price=price,
            unit_price=unit_price,
            unit=unit
        )

    total_amount += float(loading_amount)
    total_amount -= float(debit_amount)
    user_invoice.invoice_number = invoice_id
    user_invoice.total_amount = total_amount
    user_invoice.loading_amount = float(loading_amount)
    user_invoice.debit_amount = float(debit_amount)
    user_invoice.save()

    return HttpResponse("Data saved successfully")


def search_records(request):
    if request.method == 'POST':
        search_type = request.POST.get('search_type')
        search_value = request.POST.get('search_value')

        if search_type == 'user_name':
            user = User.objects.filter(name__iexact=search_value)
            invoices = Invoice.objects.filter(user__in=user)
        elif search_type == 'product_name':
            invoices = Invoice.objects.filter(items__product__name__icontains=search_value)
        elif search_type == 'phone_number':
            invoices = Invoice.objects.filter(user__phone_number__icontains=search_value)
        elif search_type == 'date':
            invoices = Invoice.objects.filter(created__date=search_value)   
            
        return render(request, 'search_results.html', {'title': f'Search by {search_type.capitalize()}', 'invoices': invoices})
    return render(request, 'homepage.html')
 

def update_invoice(request):
    if request.method == 'POST':
        debit_amounts = request.POST.getlist('debit_amounts[]')
        invoice_ids = request.POST.getlist('invoice_ids[]')

        if debit_amounts:
            for invoice_id, updated_amount in zip(invoice_ids, debit_amounts):
                if updated_amount:
                    invoice = Invoice.objects.get(id=invoice_id)
                    invoice.debit_amount = Decimal(updated_amount)
                    invoice.save()
                    messages.success(request, 'Invoices updated successfully!')
        return redirect('search_records')
    
    return render(request, 'search_results.html')


def add_product(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        product_description = request.POST.get('product_description')

        Product.objects.create(name=product_name, description=product_description)

        messages.success(request, 'Product added successfully.')
        return redirect('homepage')
