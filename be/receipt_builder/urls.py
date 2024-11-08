# url to ReceiptBuilder class
from django.urls import path
from .views import ProductManager, ReceiptBuilder

urlpatterns = [
    path('receipt_builder/', ReceiptBuilder.as_view(), name='receipt_builder'),
    path('receipt_builder/<str:receipt_id>/', ReceiptBuilder.as_view(), name='receipt_builder'),
    path('products/', ProductManager.as_view(), name='products'),
    path('products/<str:product_id>/', ProductManager.as_view(), name='products'),
]
