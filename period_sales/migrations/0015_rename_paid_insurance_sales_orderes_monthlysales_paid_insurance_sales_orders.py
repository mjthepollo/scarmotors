# Generated by Django 4.2.11 on 2024-03-29 01:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('period_sales', '0014_monthlysales_paid_insurance_sales_orderes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='monthlysales',
            old_name='paid_insurance_sales_orderes',
            new_name='paid_insurance_sales_orders',
        ),
    ]
