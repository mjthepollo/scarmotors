# Generated by Django 4.2.1 on 2023-06-26 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demand', '0041_alter_recognizedsales_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='charge',
            name='charge_date',
            field=models.DateField(blank=True, null=True, verbose_name='청구일'),
        ),
    ]
