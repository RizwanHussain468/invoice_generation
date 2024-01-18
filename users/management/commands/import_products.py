# management/commands/import_products.py
import os
from django.core.management.base import BaseCommand
from users.models import Product

class Command(BaseCommand):
    help = 'Import products from a txt file to the Product table'

    def handle(self, *args, **kwargs):
        file_path = '/home/aamir/Downloads/invoice_products.txt'

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
            return

        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line:
                    Product.objects.create(name=line)
                    self.stdout.write(self.style.SUCCESS(f"Product '{line}' imported successfully"))
