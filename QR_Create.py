import qrcode
import random
import json

destination = ["North", "South", "East", "West"]
products = ["Apple", "Banana", "Orange", "Grape", "Watermelon", "Pineapple", "Strawberry", "Mango", "Peach", "Kiwi"]
packet_number = 10

class QR_Create:
    def __init__(self):
        self.qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        self.content = ""

    def create_qr(self, id):
        self.qr.add_data(self.content)
        self.qr.make(fit=True)
        img = self.qr.make_image(fill_color="black", back_color="white")
        img.save(f"QR_{id}.png")
        self.qr.clear()

class Goods:
    _id_counter = 0

    def __init__(self):
        Goods._id_counter += 1
        self.destination = ""
        self.product = ""
        self.weight = 0
        self.weight_unit = "kg"
        self.value = 0
        self.value_unit = "USD"
        self.id = Goods._id_counter
        self.qr = QR_Create()

    def set_destination(self):
        self.destination = random.choice(destination)

    def set_product(self):
        self.product = random.choice(products)

    def set_weight(self):
        self.weight = random.randint(1, 100)
    
    def set_value(self):
        self.value = random.randint(1, 100)

    def set_content(self):
        json_content = {
            "ID": self.id,
            "Destination": self.destination,
            "Product": self.product,
            "Weight": self.weight,
            "Weight_unit": self.weight_unit,
            "Value": self.value,
            "Value_unit": self.value_unit,
        }

        json_content = json.dumps(json_content)
        self.qr.content = str(json_content)
        print (self.qr.content)

    def create_qr(self):
        self.qr.create_qr(self.id)

if __name__ == "__main__":
    packet_number = 10
    goods = []
    for i in range(packet_number):
        goods.append(Goods())
        goods[i].set_destination()
        goods[i].set_product()
        goods[i].set_weight()
        goods[i].set_value()
        goods[i].set_content()
        goods[i].create_qr()
        print(f"Packet {i+1}: {goods[i].qr.content}")
