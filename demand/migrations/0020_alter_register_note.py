# Generated by Django 4.2 on 2023-05-03 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demand', '0019_alter_order_charge_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register',
            name='note',
            field=models.TextField(blank=True, null=True, verbose_name='비고'),
        ),
    ]