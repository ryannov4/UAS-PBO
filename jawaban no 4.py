# function exception handler 
while True:
    try:
        penyebut = int(input("Masukkan angka penyebut \t: "))
        pembilang = int(input("Masukkan angka pembilang \t: "))
        hasil = penyebut/pembilang
        break
    except Exception as error:
        print(error)

print(f"Hasil pembagian nya adalah \t: {hasil}")