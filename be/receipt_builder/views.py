import asyncio
import json
import os
import cv2
from django.http import JsonResponse
from django.views import View
from ultralytics import YOLO
from channels.layers import get_channel_layer
from ws_camera.models import Product, Receipt
from asgiref.sync import sync_to_async

# Helper Functions
@sync_to_async
def get_receipt_by_id(receipt_id):
    try:
        return Receipt.objects.filter(receipt_id=receipt_id).first()
    except Exception as e:
        raise Exception(f"Error getting receipt by id: {e}")

@sync_to_async
def get_product_by_name(product_name):
    try:
        return Product.objects.filter(product_name=product_name).first()
    except Exception as e:
        raise Exception(f"Error getting product by name: {e}")

@sync_to_async
def create_product(product_name, price=0, description=''):
    try:
        product = Product.objects.create(product_name=product_name, product_price=price, description=description)
        product.save()
        return product
    except Exception as e:
        raise Exception(f"Error creating product: {e}")

@sync_to_async
def create_receipt(receipt_id, total_price=0):
    try:
        receipt = Receipt.objects.create(receipt_id=receipt_id, total_price=total_price)
        receipt.save()
        return receipt
    except Exception as e:
        raise Exception(f"Error creating receipt: {e}")

@sync_to_async
def add_product_to_receipt(receipt, product, weight):
    try:
        if product not in receipt.product.all():
            receipt.product.add(product)
        receipt.total_price += product.product_price * weight
        receipt.save()
    except Exception as e:
        raise Exception(f"Error adding product to receipt: {e}")

@sync_to_async
def generate_response(receipt, product, weight):
    response = {
        'receipt': {
            'receipt_id':str(receipt.receipt_id),
            'product': product,
            'weight': weight,
            'total_price': receipt.total_price,
        }
    }
    receipt.data = response
    receipt.save()
    return response

async def wait_for_image(image_file_name, timeout=5):
    start_time = asyncio.get_event_loop().time()
    while not os.path.exists(image_file_name):
        await asyncio.sleep(1)
        if asyncio.get_event_loop().time() - start_time > timeout:
            return False
    return True

async def process_image(image_file_name):
    try:
        image = cv2.imread(image_file_name)
        image = cv2.resize(image, (640, 640))
        model = YOLO('../best.pt')
        results = model(image)
        return results[0]
    except Exception as e:
        print(f"Error in process_image: {e}")
        return None

class ReceiptBuilder(View):
    async def get(self, request, receipt_id=None):
        if not receipt_id:
            results = await sync_to_async(list)(Receipt.objects.all())
        else:
            results = await sync_to_async(list)(Receipt.objects.filter(receipt_id=receipt_id))

        response = {}
        for receipt in results:
            response[str(receipt.receipt_id)] = receipt.data

        return JsonResponse(response, status=200)

    async def post(self, request):
        try:
            data = json.loads(request.body)
            receipt_id = data.get('receipt_id', None)
            weight = data.get('weight')
            print(data)


            # Comment ìf you don't have a camera
            # channel_layer = get_channel_layer()
            # await channel_layer.group_send(
            #     "capture_group",
            #     {"type": "receive_capture_command"},
            # )

            # After comment, fake image file
            image_file_name = r'D:\Ky_7\IoT\apple.jpg'
            # original.
            # image_file_name = "image_png"
            if not await wait_for_image(image_file_name):
                return JsonResponse({"error": "Timeout waiting for image file"}, status=500)

            result = await process_image(image_file_name)
            cls_id = '-1'
            if result and result.boxes:
                cls_id = result.boxes.cls.cpu().numpy()[0]

            # original, comment for test
            # os.remove(image_file_name)

            if cls_id == '-1':
                return JsonResponse({"error": "No product detected"}, status=404)

            product_name = result.names[cls_id]
            product = await get_product_by_name(product_name)
            if not product:
                product = await create_product(product_name)

            # Mapping english name to vietnamese name
            legal_product_name = self.fruitname_mapping(product_name)

            receipt = await get_receipt_by_id(receipt_id)
            if not receipt:
                receipt = await create_receipt(receipt_id)
            await add_product_to_receipt(receipt, product, weight)

            response = await generate_response(receipt, legal_product_name, weight)
            return JsonResponse(response, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def fruitname_mapping(self, product_name):
        if product_name == 'apple':
            return 'Táo'
        elif product_name == 'banana':
            return 'Chuối'
        elif product_name == 'orange':
            return 'Cam'
        elif product_name == 'watermelon':
            return 'Dưa hấu'
        elif product_name == 'grape':
            return 'Nho'
        elif product_name == 'mango':
            return 'Xoài'
        elif product_name == 'pear':
            return 'Lê'
        elif product_name == 'pineapple':
            return 'Dứa'
        elif product_name == 'guava':
            return 'Ổi'
        elif product_name == 'bell_pepper':
            return 'Ớt chuông'
        elif product_name == 'Lady finger':
            return 'Đậu bắp'

class ProductManager(View):
    def get(self, request):
        products = Product.objects.all()
        response = {
            "products": [
                {
                    "product_id": product.product_id,
                    "product_name": product.product_name,
                    "price": product.product_price,
                    "description": product.description,
                }
                for product in products
            ]
        }
        return JsonResponse(response, status=200)

    def post(self, request):
        try:
            data = json.loads(request.body)
            product_name = data.get('product_name')
            price = data.get('price', 0)
            description = data.get('description', '')

            product = Product.objects.create(product_name=product_name, product_price=price, description=description)
            product.save()
            return JsonResponse({"product_id": product.product_id, "price": product.product_price}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def put(self, request, product_id):
        try:
            data = json.loads(request.body)
            print(data)
            product = Product.objects.filter(product_id=product_id).first()
            if not product:
                return JsonResponse({"error": "Product not found"}, status=404)
            product.product_price = data.get('price', product.product_price)
            print(product.product_price)
            product.save()
            return JsonResponse({'product_id': product.product_id, 'price': product.product_price}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)