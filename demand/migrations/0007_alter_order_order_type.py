# Generated by Django 4.2 on 2023-04-25 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demand', '0006_alter_order_fault_ratio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_type',
            field=models.CharField(blank=True, choices=[('자차', '자차'), ('대물', '대물'), ('일반', '일반')], max_length=10, null=True, verbose_name='차/대/일'),
        ),
    ]