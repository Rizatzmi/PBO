# Class pertama: DataPribadi
class DataPribadi:

    def __init__(self, nama, umur):
        self.__nama = nama      # enkapsulasi private attribute
        self.__umur = umur

    @property
    def nama(self):
        return self.__nama

    @property
    def umur(self):
        return self.__umur

    @nama.setter
    def nama(self, input):
        self.__nama = input

    @umur.setter
    def umur(self, input):
        if input >= 0:
            self.__umur = input
        else:
            print("Usia tidak valid")


# ==========================================================
# Class kedua: Akademik
# ==========================================================

class Akademik:

    def __init__(self, nim, prodi):
        self.__nim = nim        # enkapsulasi private attribute
        self.__prodi = prodi

    @property
    def nim(self):
        return self.__nim

    @property
    def prodi(self):
        return self.__prodi

    @nim.setter
    def nim(self, input):
        self.__nim = input

    @prodi.setter
    def prodi(self, input):
        self.__prodi = input

# ==========================================================
# Class Mahasiswa yang mewarisi DataPribadi dan Akademik
# ==========================================================

class Mahasiswa(DataPribadi, Akademik):

    def __init__(self, nama, umur, nim, prodi):
        DataPribadi.__init__(self, nama, umur)
        Akademik.__init__(self, nim, prodi)

    def info_mahasiswa(self):
        return (f"Nama: {self.nama}, Usia: {self.umur}, "
                f"NIM: {self.nim}, Jurusan: {self.prodi}")

    def ubah_jurusan(self, prodi_baru):
        self.prodi = prodi_baru
        print(f"Jurusan diubah menjadi {self.prodi}")


# ==========================================================
# Program Utama
# ==========================================================

class Sistem:
    
    def __init__(self):
        self.daftar_mahasiswa = []
    
    def jalankan(self):
        while True:
            print("\n" + "="*50)
            print("SISTEM MANAJEMEN DATA MAHASISWA")
            print("="*50)
            print("1. Tambah Mahasiswa")
            print("2. Tampilkan Data Mahasiswa")
            print("3. Keluar")
            print("="*50)
            
            pilihan = input("Pilih menu (1/2/3): ")
            
            if pilihan == "1":
                self.tambah_mahasiswa()
            elif pilihan == "2":
                self.tampilkan_mahasiswa()
            elif pilihan == "3":
                print("Terima kasih! Program ditutup.")
                break
            else:
                print("Menu tidak valid! Silakan pilih 1, 2, atau 3.")
    
    def tambah_mahasiswa(self):
        print("\n--- TAMBAH MAHASISWA ---")
        jumlah_input = input("Berapa mahasiswa yang ingin ditambahkan? ")
        
        if not jumlah_input.isdigit():
            print("Jumlah harus berupa angka!")
            return
        
        jumlah = int(jumlah_input)
        
        for i in range(jumlah):
            print(f"\nData Mahasiswa {i+1}:")
            nama = input("Masukkan nama: ")
            umur_input = input("Masukkan usia: ")
            nim_input = input("Masukkan NIM: ")
            prodi = input("Masukkan jurusan: ")
            
            if not umur_input.isdigit():
                print("Usia harus berupa angka!")
                continue
            
            if not nim_input.isdigit():
                print("NIM harus berupa angka!")
                continue
            
            umur = int(umur_input)
            nim = nim_input
            
            mhs = Mahasiswa(nama, umur, nim, prodi)
            self.daftar_mahasiswa.append(mhs)
            print(f"Mahasiswa {nama} berhasil ditambahkan!")
    
    def tampilkan_mahasiswa(self):
        print("\n--- DATA MAHASISWA ---")
        if not self.daftar_mahasiswa:
            print("Belum ada data mahasiswa.")
        else:
            for i, mhs in enumerate(self.daftar_mahasiswa, 1):
                print(f"{i}. {mhs.info_mahasiswa()}")

program = Sistem()
program.jalankan()