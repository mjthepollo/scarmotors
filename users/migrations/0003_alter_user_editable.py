# Generated by Django 4.2 on 2023-05-04 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_editable_user_first_name_user_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='editable',
            field=models.BooleanField(default=False, verbose_name='수정권한'),
        ),
    ]
