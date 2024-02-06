# Generated by Django 5.0 on 2024-02-06 02:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_alter_order_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='phone',
            field=models.CharField(null=True, unique=True, validators=[django.core.validators.RegexValidator('^\\+?\\d{1,15}$', 'Введите корректный номер телефона.')], verbose_name='Телефон'),
        ),
    ]