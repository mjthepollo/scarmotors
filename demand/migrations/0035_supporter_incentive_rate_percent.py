# Generated by Django 4.2.1 on 2023-06-26 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demand', '0034_rename_first_center_register_first_center_repaired'),
    ]

    operations = [
        migrations.AddField(
            model_name='supporter',
            name='incentive_rate_percent',
            field=models.IntegerField(default=85, verbose_name='지급율'),
        ),
    ]