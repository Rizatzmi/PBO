class Mhs:
    institusi = "Insitut Teknologi dan Bisnis Asia Malang"
    jumlah_mhs = 0

    def __init__(self, nama, nim, nilai):
        self.__nama = nama
        self.__nim = nim
        self.__nilai = nilai
        Mhs.jumlah_mhs += 1


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

    @property
    def nilai(self):
        return self.__nilai
    
    @nilai.setter
    def nilai(self, value):
        if 0 <= value <= 100:
            self.__nilai = value
        else:
            print("Nilai harus antara 0 dan 100")

    @nilai.deleter
    def nilai(self):
        print(f"Menghapus data nilai untuk {self.__nama}")
        self.__nilai = 0

    @staticmethod
    def cek_kelulusan(nilai):
        if nilai >= 60:
            return "Lulus"
        else:
            return "Tidak Lulus"
    
    def get_grade(self):
        if self.__nilai < 50:
            return "E"
        elif self.__nilai < 55:
            return "D"
        elif self.__nilai < 65:
            return "C"
        elif self.__nilai < 80:
            return "B"
        else:
            return "A"
        
    @classmethod
    def ubah_institusi(cls, nama_baru):
        cls.institusi = nama_baru
        print(f"Institusi diubah menjadi {cls.institusi}")
    
    def tampilkan_tabel(daftar_mhs):
        print(f"\nData seluruh mahasiswa : {Mhs.institusi}")
        print("="*75)
        print(f"{'NO':<5} {'NIM':<15} {'NAMA':<20} {'NILAI':<10} {'GRADE':<10}")
        print("="*75)
        
        for idx, mhs in enumerate(daftar_mhs, 1):
            grade = mhs.get_grade()
            print(f"{idx:<5} {mhs.nim:<15} {mhs.nama:<20} {mhs.nilai:<10} {grade:<10}")
        
        print("="*75)

# ===== INPUT KEYBOARD =====
print("\n" + "="*50)
print("PROGRAM INPUT MAHASISWA")
print("="*50)

jumlah_mhs_input = int(input("\nBerapa jumlah mahasiswa yang ingin dimasukkan? "))

daftar_mhs = []

for i in range(jumlah_mhs_input):
    print(f"\n--- Data Mahasiswa {i+1} ---")
    nim = input("Masukkan NIM: ")
    nama = input("Masukkan nama mahasiswa: ")
    
    while True:
        try:
            nilai = int(input("Masukkan nilai (0-100): "))
            if 0 <= nilai <= 100:
                break
            else:
                print("Nilai harus antara 0 dan 100!")
        except ValueError:
            print("Masukkan nilai dengan benar!")
    
    mhs = Mhs(nama, nim, nilai)
    daftar_mhs.append(mhs)

Mhs.tampilkan_tabel(daftar_mhs)