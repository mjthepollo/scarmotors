# Generated by Django 4.2.1 on 2023-08-11 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('period_sales', '0011_delete_statisticsales'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monthlysales',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='생성시각'),
        ),
        migrations.AlterField(
            model_name='monthlysales',
            name='updated',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='수정시각'),
        ),
    ]