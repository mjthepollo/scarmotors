# Generated by Django 4.2.1 on 2023-06-30 21:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('period_sales', '0005_alter_monthlysales_not_paid_turnover_info_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monthlysales',
            name='not_paid_turnover_info',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='period_sales.notpaidturnoversalesinfo', verbose_name='미입금매출'),
        ),
        migrations.AlterField(
            model_name='monthlysales',
            name='paid_turnover_info',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='period_sales.paidturnoversalesinfo', verbose_name='입금매출'),
        ),
        migrations.AlterField(
            model_name='statisticsales',
            name='not_paid_turnover_info',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='period_sales.notpaidturnoversalesinfo', verbose_name='미입금매출'),
        ),
        migrations.AlterField(
            model_name='statisticsales',
            name='paid_turnover_info',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='period_sales.paidturnoversalesinfo', verbose_name='입금매출'),
        ),
    ]