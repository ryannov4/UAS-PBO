#Polymorphism
class makan:
    def mengkonsumsi(self):
        return 'makanan pedas'

class minum:
    def mengkonsumsi(self):
        return 'minuman soda'

obj_makanan = makan()
obj_minuman = minum()

for obj in [obj_makanan, obj_minuman]:
    print(obj.mengkonsumsi())