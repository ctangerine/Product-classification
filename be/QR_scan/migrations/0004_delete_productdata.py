# Generated by Django 5.0.3 on 2024-09-04 02:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('QR_scan', '0003_remove_productdata_id_alter_productdata_product_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProductData',
        ),
    ]
