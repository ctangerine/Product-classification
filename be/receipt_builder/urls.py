# url to ReceiptBuilder class
from django.urls import path
from .views import ReceiptBuilder

urlpatterns = [
    path('receipt_builder/', ReceiptBuilder.as_view(), name='receipt_builder')
]
