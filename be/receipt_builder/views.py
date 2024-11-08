import asyncio
import json
import os
import cv2
from django.http import JsonResponse
from django.views import View
from ultralytics import YOLO
from channels.layers import get_channel_layer

class ReceiptBuilder(View):
    async def get(self, request):
        pass

    async def post(self, request):
        try:
            data = json.loads(request.body)
            print(data)
            #time = data['time']
            weight = data['weight']

            channel_layer = get_channel_layer()
            await channel_layer.group_send(
                "capture_group",
                {
                    "type": "receive_capture_command",
                },
            )

            image_file_name = "image.png"
            start_time = asyncio.get_event_loop().time()
            while not os.path.exists(image_file_name):
                await asyncio.sleep(1)
                if asyncio.get_event_loop().time() - start_time > 5:
                    return JsonResponse({"error": "Timeout waiting for image file"}, status=500)

            result = await self.process_image(image_file_name)
            cls_id = '-1'
            if result and result[0].boxes:
                cls_id = result[0].boxes.cls.cpu().numpy()[0]
              
            # delete "image.png"
            os.remove(image_file_name)
            print(cls_id)
            return JsonResponse({"result": result.names[cls_id]})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    async def process_image(self, image_file_name):
        try:
            image = cv2.imread(image_file_name)
            image = cv2.resize(image, (640, 640))

            model = YOLO('../best.pt')
            results = model(image)
            return results[0]
        except Exception as e:
            print(f"Error in process_image: {e}")
            return None