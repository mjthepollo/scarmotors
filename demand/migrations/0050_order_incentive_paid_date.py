# Generated by Django 4.2.1 on 2023-07-04 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demand', '0049_mockupcreated'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='incentive_paid_date',
            field=models.DateField(blank=True, null=True, verbose_name='인센티브 지급일'),
        ),
    ]
