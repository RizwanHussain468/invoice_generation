# Generated by Django 4.1.7 on 2023-12-27 01:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_invoiceitem_debit_amount_invoiceitem_loading_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user', to_field='phone_number'),
        ),
    ]