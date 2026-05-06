class Mhs:
    __jumlah = 0;
    def __init__(self, nama, umur):
        self.__nama = nama
        self.__umur = umur
        Mhs.__jumlah += 1

    def get_nama(self):
        return self.__nama
        
    def set_nama(self, nama_baru):
        self.__nama = nama_baru

    def get_umur(self):
        return self.__umur
        
    def set_umur(self, umur_baru):
        if umur_baru > 0:
            self.__umur = umur_baru
        else:
            print("Umur harus positif")
    
    def get_jumlah(self):
        return Mhs.__jumlah
    
    def get_jumlah2():
        return Mhs.__jumlah
    
    @staticmethod
    def get_jumlah3():
        return Mhs.__jumlah

mhs_asia = Mhs("Andi", 20)

print(mhs_asia.get_jumlah())
# print(Mhs.get_jumlah())

# print(mhs_asia.get_jumlah2())
print(Mhs.get_jumlah2())

print("---Static Method---")

print(mhs_asia.get_jumlah3())
print(Mhs.get_jumlah3())