# Generated by Django 5.0.7 on 2024-08-06 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_store_app', '0010_orders_shipping_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='shipping_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('shipped', 'Shipped'), ('delivered', 'Delivered'), ('returned', 'Returned')], default='pending', max_length=10),
        ),
    ]
