# Generated by Django 5.0.3 on 2024-11-08 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ws_camera', '0010_alter_product_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receipt',
            name='total_price',
            field=models.FloatField(default=0),
        ),
    ]