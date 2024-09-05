from django.contrib import admin
from .models import ProductData

# Register your models here.
@admin.register(ProductData)
class ProductTrackingAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'destination', 'product', 'weight', 'weight_unit', 'value', 'value_unit', 'qr_data', 'recorded_at')
    search_fields = ('product_id', 'destination', 'product', 'weight', 'weight_unit', 'value', 'value_unit', 'qr_data')