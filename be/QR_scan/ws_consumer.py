import asyncio
import base64
import json
import time
from .models import ProductData
from channels.generic.websocket import AsyncWebsocketConsumer
from QR_scan.img_process_helper.change_detection import ChangeDetection
from QR_scan.img_process_helper.QR_reader import QRReader
from QR_scan.models import ProductData
from asgiref.sync import sync_to_async

class CamWSConsumer(AsyncWebsocketConsumer):
    '''
    Core consumer class for handling WebSocket connections.
    '''
    async def connect(self):
        self.type = None
        try:
            print('New ws consumer connected')
            await self.accept()
            await self.send_handshake()
        except Exception as error:
            print('Error in connection with camera: ', error)

    async def disconnect(self, close_code):
        try:
            await self.remove_from_group()
            await self.cleanup_resources()
        except Exception as e:
            print(f"Error: {e}")

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            try:
                t_data = json.loads(text_data)

                if 'message' not in t_data:
                    return

                message = t_data['message']

                if message == 'new camera':
                    await self.setup_camera()
                elif message == 'new client':
                    await self.setup_client()

                if 'image' in t_data:
                    image_base64 = t_data['image']
                    image_bytes = base64.b64decode(image_base64)

                    if self.type == 'camera':
                        await self.handle_bytes_data(message, image_bytes)
            except json.JSONDecodeError:
                print("Received invalid JSON")
            except Exception as e:
                print(f"Error in receving data: {e}")

    '''
    Helper functions
    '''
    async def send_handshake(self):
        await self.send(text_data=json.dumps({
            'message': 'handshake'
        }))

    async def remove_from_group(self):
        await self.channel_layer.group_discard(
            'cameras',
            self.channel_name
        )

    async def cleanup_resources(self):
        if self.type == 'camera':
            if hasattr(self, 'detector'):
                del self.detector
            if hasattr(self, 'qr_decoder'):
                del self.qr_decoder
            print(f"Camera disconnected\n")
        elif self.type == 'client':
            print(f"Client disconnected\n")

    async def setup_camera(self):
        self.type = 'camera'
        print(f"Camera connected")
        self.detector = ChangeDetection()
        self.qr_decoder = QRReader()
        await self.send(text_data=json.dumps({
            'message': 'send_original_frame'
        }))
        await self.channel_layer.group_add(
            'cameras',
            self.channel_name
        )

    async def setup_client(self):
        self.type = 'client'
        print(f"Client connected\n")
        await self.channel_layer.group_add(
            'clients',
            self.channel_name
        )

    async def handle_bytes_data(self, message, bytes_data):
        try:
            if message == 'original_frame':
                start_time = time.time()
                await self.process_original_frame(bytes_data)
                print('FPS processable for first frame: ', 1 / (time.time() - start_time))
            elif message == 'discrete_frame':
                start_time = time.time()
                await self.process_discrete_frame(bytes_data)
                print('FPS processable for discrete frame: ', 1 / (time.time() - start_time))
            elif message == 'continuous_frame':
                start_time = time.time()
                await self.process_continuous_frame(bytes_data)
                print('FPS processable for continuous frame: ', 1 / (time.time() - start_time))
        except json.JSONDecodeError:
            print("Received invalid JSON")
        except Exception as e:
            print(f"Error in handle data's message: {e}")

    async def process_original_frame(self, bytes_data):
        try:
            await self.detector.set_original_image(bytes_data)
            await self.send(text_data=json.dumps({
                'message': 'send_discrete_frame',
                'time_between': 0.3
            }))
        except Exception as e:
            print(f"Error: {e}")
            await self.send(text_data=json.dumps({
                'message': 'send_original_frame'
            }))

    async def process_discrete_frame(self, bytes_data):
        change_detected = await self.detector.detect_and_notify(bytes_data)
        if change_detected:
            await self.send(text_data=json.dumps({
                'message': 'send_continuous_frame'
            }))

    async def process_continuous_frame(self, bytes_data):
        qr_data = await self.qr_decoder.read_qr_code(bytes_data)
        if qr_data:
            try:
                data = json.loads(qr_data)
                await asyncio.gather(
                    self.record_product_data(data),
                    self.send(text_data=json.dumps({
                        'message': 'send_discrete_frame'
                    }))
                )
            except json.JSONDecodeError:
                print("Received invalid JSON from qr code data")
                print(f"QR data: {qr_data}")
                return
            except Exception as e:
                print(f"Error in processing continuous frame: {e}")
                return

    async def record_product_data(self, data):
        try:
            product = ProductData(
                product_id=data['ID'],
                destination=data['Destination'],
                product=data['Product'],
                weight=data['Weight'],
                weight_unit=data['Weight_unit'],
                value=data['Value'], 
                value_unit=data['Value_unit'],
                
                qr_data = f'Product id: {data["ID"]}, Destination: {data["Destination"]}, product type: {data["Product"]}, weight: {data["Weight"]} {data["Weight_unit"]}, value: {data["Value"]} {data["Value_unit"]}'
            )
            await sync_to_async(product.save)()
        except Exception as e:
            print(f"Error in adding product data: {e}")

