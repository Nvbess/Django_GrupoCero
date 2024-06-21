# Generated by Django 5.0.6 on 2024-06-21 05:06

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_carrito_itemcarrito'),
    ]

    operations = [
        migrations.CreateModel(
            name='Voucher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.CharField(max_length=255)),
                ('payer_id', models.CharField(max_length=255)),
                ('order_id', models.CharField(max_length=255)),
                ('payment_token', models.CharField(max_length=255)),
                ('return_url', models.URLField()),
                ('details', models.JSONField()),
            ],
        ),
        migrations.AlterField(
            model_name='arte',
            name='imagen',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='imagen'),
        ),
        migrations.AlterField(
            model_name='autor',
            name='imagen',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='imagen'),
        ),
    ]