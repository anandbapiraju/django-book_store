# Generated by Django 5.0.7 on 2024-08-06 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_store_app', '0009_orders_address_orders_phone_number_orders_pincode'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='shipping_status',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
