class Mhs:
    def __init__(self, nama, nim):
        self.__nama = nama
        self.__nim = nim

    @property
    def nama(self):
        return self.__nama
        
    @nama.setter
    def nama(self, value):
        if not value:
            raise ValueError("Nama tidak boleh kosong")
        self.__nama = value

    @property
    def nim(self):
        return self.__nim
        
    @nim.setter
    def nim(self, value):
        self.__nim = value

mhs_asia = Mhs("Andi", 1234567890)
print(mhs_asia.nama)
print(mhs_asia.nim)

mhs_asia.nama = "Budi"
mhs_asia.nim = 12345
print(mhs_asia.nama)
print(mhs_asia.nim)
