# Generated by Django 4.2.1 on 2023-05-05 02:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demand', '0025_alter_charge_options_alter_chargedcompany_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='extrasales',
            options={'ordering': ['-created'], 'verbose_name': '기타 매출', 'verbose_name_plural': '기타 매출(들)'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-created'], 'verbose_name': '주문 매출', 'verbose_name_plural': '주문 매출(들)'},
        ),
    ]