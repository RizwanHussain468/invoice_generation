import pytz

from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

from .models import User, Invoice, InvoiceItem, Product
from django.utils import timezone
from django.core.serializers import serialize



def homepage_view(request):
    return render(request, 'homepage.html')


def create_user(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone_number = request.POST.get('phone')

        existing_user = User.objects.filter(phone_number=phone_number).first()

        if existing_user:
            existing_invoice = Invoice.objects.filter(invoice_number__isnull=False).last()
            print(existing_invoice)

            if not existing_invoice:
                new_invoice = Invoice.objects.create(user=existing_user)
                print("new ", new_invoice)
                invoice_id = new_invoice.id
            else:
                invoice_id = existing_invoice.invoice_number + 1
            print("idd ", invoice_id)
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
    print("Received data:", request.POST)

    name = request.POST.get('name')
    phone = request.POST.get('phone')
    invoice_id = request.POST.get('invoice_id')
    loading_amount = request.POST.get('loading_amount')
    debit_amount = request.POST.get('debit_amount')

    unit_price_list = request.POST.getlist('unit_price')
    quantity_list = request.POST.getlist('quantity')
    product_list = request.POST.getlist('product')
    unit_list = request.POST.getlist('unit')

    print("Name:", name)
    print("Phone:", phone)
    print("Invoice:", invoice_id)
    print("Loading Amount:", loading_amount)
    print("Debit Amount:", debit_amount)

    print("Unit Prices:", unit_price_list)
    print("Quantities:", quantity_list)
    print("Products:", product_list)
    print("Units:", unit_list)

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

    messages.success(request, 'Data saved successfully')
    return redirect('invoice', invoice_id=user_invoice.id, user_id=user.id)


def get_products(request):
    products = Product.objects.all()
    # Serialize the queryset to JSON
    serialized_products = serialize('json', products)
    
    return JsonResponse({'products': serialized_products})
 