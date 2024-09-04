# Generated by Django 5.0.3 on 2024-09-04 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('QR_scan', '0004_delete_productdata'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductData',
            fields=[
                ('product_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('destination', models.CharField(max_length=50)),
                ('product', models.CharField(max_length=50)),
                ('weight', models.CharField(max_length=50)),
                ('weight_unit', models.CharField(max_length=50)),
                ('value', models.CharField(max_length=50)),
                ('value_unit', models.CharField(max_length=50)),
                ('qr_data', models.CharField(max_length=100)),
                ('recorded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
