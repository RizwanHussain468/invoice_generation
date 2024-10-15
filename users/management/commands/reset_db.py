from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Reset the ID sequence for a table'

    def add_arguments(self, parser):
        parser.add_argument('table_name', type=str, help='Name of the table to reset the ID sequence for')

    def handle(self, *args, **kwargs):
        table_name = kwargs['table_name']
        with connection.cursor() as cursor:
            cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table_name}'")
        self.stdout.write(self.style.SUCCESS(f"Successfully reset ID sequence for {table_name}"))
