# Generated by Django 4.2 on 2023-04-25 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demand', '0005_alter_register_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='fault_ratio',
            field=models.IntegerField(blank=True, null=True, verbose_name='과실분'),
        ),
    ]