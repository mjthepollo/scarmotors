# Generated by Django 4.2.1 on 2023-06-26 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demand', '0039_requestdepartment_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='register',
            name='wash_car',
        ),
        migrations.AlterField(
            model_name='extrasales',
            name='sort',
            field=models.CharField(choices=[('세차', '세차'), ('기타', '기타')], max_length=20, verbose_name='구분'),
        ),
    ]