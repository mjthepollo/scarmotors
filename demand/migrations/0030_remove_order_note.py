# Generated by Django 4.2.1 on 2023-06-25 06:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demand', '0029_alter_order_charged_company'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='note',
        ),
    ]