import uuid
from django.db import models

# Create your models here.

class Product(models.Model):
    product_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    product_name = models.CharField(max_length=100)
    product_price = models.FloatField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.product_name
class Receipt(models.Model):
    receipt_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    product = models.ManyToManyField(Product)
    total_price = models.FloatField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    data = models.JSONField(default=dict)

    def __str__(self):
        return self.recept_id

