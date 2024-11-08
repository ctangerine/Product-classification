import os
import logging
from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger(__name__)

class CamWSConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            await self.accept()
            await self.channel_layer.group_add("capture_group", self.channel_name)
            logger.info("WebSocket connection established")
        except Exception as e:
            logger.error(f"Error during WebSocket connection: {e}")

    async def disconnect(self, close_code):
        try:
            await self.channel_layer.group_discard("capture_group", self.channel_name)
            await self.close()
            logger.info(f"WebSocket connection closed with code {close_code}")
        except Exception as e:
            logger.error(f"Error during WebSocket disconnection: {e}")

    async def receive(self, text_data=None, bytes_data=None):
        try:
            if bytes_data:
                logger.info('Received byte data')
                os.makedirs('images', exist_ok=True)

                image_file_name = "image.png"
                with open(image_file_name, 'wb') as file:
                    file.write(bytes_data)
                    logger.info('Image saved')
        except Exception as e:
            logger.error(f"Error during receiving data: {e}")

    async def receive_capture_command(self, event):
        try:
            await self.send(text_data='capture')
            logger.info("Sent 'capture' command to camera")
        except Exception as e:
            logger.error(f"Error during sending capture command: {e}")