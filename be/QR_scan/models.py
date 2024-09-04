from django.db import models

# Create your models here.
class ProductData(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)
    product = models.CharField(max_length=50)
    weight = models.CharField(max_length=50)
    weight_unit = models.CharField(max_length=50)
    value = models.CharField(max_length=50)
    value_unit = models.CharField(max_length=50)
    qr_data = models.CharField(max_length=100)
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.qr_data
