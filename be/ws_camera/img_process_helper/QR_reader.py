import cv2
import time

import numpy as np

class QRReader:
    def __init__(self):
        self.qr_code = cv2.QRCodeDetector()

    async def read_qr_code(self, image):
        if isinstance(image, bytes):
            image = np.frombuffer(image, np.uint8)
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        data, _, _ = self.qr_code.detectAndDecode(image)
        if data:
            return data
        else:
            print("QR Code not detected")
            return None
        