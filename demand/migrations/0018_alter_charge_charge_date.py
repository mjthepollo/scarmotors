# Generated by Django 4.2 on 2023-05-02 00:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('demand', '0017_alter_order_charged_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='charge',
            name='charge_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='청구일'),
            preserve_default=False,
        ),
    ]
