#inheritance
class Product:
    def __init__(self, id, nama):
        self.id = id
        self.nama = nama
        
class Brand(Product):
    def __init__(self, id, nama, harga):
        self.harga = harga
        Product.__init__(self, id, nama)
    def brDisp(self):
        print(self.id,"-", self.nama,"Harga", self.harga)

test = Brand(1,'Ultora Milek',4000)
test2 = Brand(2,'Susu Beruang',6000)
 
test.brDisp()
test2.brDisp()