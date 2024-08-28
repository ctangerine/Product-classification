import cv2
import time

class QR_Reader:
    def __init__(self):
        self.qr_code = cv2.QRCodeDetector()

    def read_qr_code(self, image):
        data, bbox, straight_qrcode = self.qr_code.detectAndDecode(image)
        if data:
            print (f"Decoded data: {data}")
        else:
            print("QR Code not detected")
        return data, bbox, straight_qrcode
    
def main():
    qr_reader = QR_Reader()
    # for i in range(10):
    #     start_time = time.time()
    #     image = cv2.imread(f'QR_{i+1}.png')
    #     data, _ , _ = qr_reader.read_qr_code(image)
    #     print(f"FPS : {1/(time.time() - start_time)}")
    #     print(data)
    start_time = time.time()
    image = cv2.imread(r'C:\Users\Lenovo\OneDrive - The University of Technology\Desktop\Group 2.png')
    data, _ , _ = qr_reader.read_qr_code(image)
    print(f"FPS : {1/(time.time() - start_time)}")
    print(data)

main()