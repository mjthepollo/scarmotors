# Generated by Django 4.2.1 on 2023-06-26 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demand', '0032_remove_extrasales_unrepaired_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='register',
            name='first_center',
            field=models.BooleanField(default=False, verbose_name='1센터 수리건'),
        ),
    ]