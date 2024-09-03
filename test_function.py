import asyncio
import websockets
import json
import base64

async def send_message(websocket, message_type, data=None):
    message = {'message': message_type}
    await websocket.send(json.dumps(message))
    print(f"Sent: {message}")

async def send_frame(websocket, message_type, file_path):
    with open(file_path, 'rb') as file:
        image_bytes = file.read()
        
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        
        data_to_send = json.dumps({
            'message': message_type,
            'image': image_base64
        })
        
        # Gửi JSON đã tạo
        await websocket.send(data_to_send)

async def receive_message(websocket):
    response = await websocket.recv()
    data = json.loads(response)
    print(f"Received: {data}")
    return data

async def simulate_camera(uri):
    async with websockets.connect(uri) as websocket:
        # Send initial connection message as 'new camera'
        await send_message(websocket, 'new camera')

        while True:
            # Receive message from server
            response = await receive_message(websocket)
            message_type = response.get('message')

            if message_type == 'send_original_frame':
                # Simulate sending an original frame (as byte data)
                await send_frame(websocket, 'original_frame', r'E:\DUT Courses\Academic year 4\IOT\Product-classification\QR images\org_image.png')
                print("Sent okay")
            
            elif message_type == 'send_discrete_frame':
                # Simulate sending discrete frames (as byte data)
                await send_frame(websocket, 'discrete_frame', r'E:\DUT Courses\Academic year 4\IOT\Product-classification\QR images\concrete_img.png')
                print ('send discrete frame')

            elif message_type == 'send_continuous_frame':
                # Simulate sending continuous frames (as byte data)
                await send_frame(websocket, 'continuous_frame', r'E:\DUT Courses\Academic year 4\IOT\Product-classification\QR images\new_igm.png')
                print ('send continuous frame')

            # Add any additional logic here based on different message types
            # For example, you can handle specific commands or signals from the server.

async def main():
    uri = "ws://localhost:8000/ws/"  # Change this URI to your server's WebSocket endpoint
    await simulate_camera(uri)

if __name__ == "__main__":
    asyncio.run(main())

# Chạy hàm main
asyncio.run(main())

#    # Gửi khung hình gốc
#         await send_frame(websocket, 'original_frame', r'E:\DUT Courses\Academic year 4\IOT\Product-classification\QR images\org_image.png')
#         await asyncio.sleep(2)  # Đợi server phản hồi

#         # Gửi khung hình phân tán
#         await send_frame(websocket, 'discrete_frame', r'E:\DUT Courses\Academic year 4\IOT\Product-classification\QR images\concrete_img.png')
#         await asyncio.sleep(2)  # Đợi server phản hồi

#         # Gửi khung hình liên tục
#         await send_frame(websocket, 'continuous_frame', r'E:\DUT Courses\Academic year 4\IOT\Product-classification\QR images\new_igm.png')
#         await asyncio.sleep(2)  # Đợi server phản hồi