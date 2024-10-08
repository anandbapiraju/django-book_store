# Generated by Django 5.0.7 on 2024-07-31 08:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_store_app', '0004_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='book_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='book_store_app.book'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cart',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]
