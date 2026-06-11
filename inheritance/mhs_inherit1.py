import datetime
import random

# 1. Kelas Induk: Mahasiswa
class Mahasiswa:
    def __init__(self, nama):
        self.nama = nama
        self.tahun_sekarang = datetime.datetime.now().year
        self.nim = ""
        self.maks_kuliah = 0

    def generate_nim(self, kode_program):
        # Ambil 2 digit terakhir dari tahun sekarang (contoh: 2026 -> "26")
        dua_digit_tahun = str(self.tahun_sekarang)[-2:]

        # Generate 3 digit angka random antara 100 sampai 999
        tiga_digit_random = str(random.randint(100, 999))

        # Gabungkan semua komponen NIM
        self.nim = f"{dua_digit_tahun}{kode_program}{tiga_digit_random}"

    def hitung_batas_tahun(self, durasi_maksimal):
        # Tahun batas maksimal kuliah
        return self.tahun_sekarang + durasi_maksimal

    def tampilkan_info(self):
        print("\n======================================")
        print("      DATA MAHASISWA BERHASIL DICATAT")
        print("======================================")
        print(f"Nama            : {self.nama}")
        print(f"NIM (Generated) : {self.nim}")
        print(f"Tahun Masuk     : {self.tahun_sekarang}")

        # Menghitung tahun batas akhir berdasarkan durasi maksimal masing-masing kelas anak
        tahun_batas = self.hitung_batas_tahun(self.maks_kuliah)

        print(f"NOTIFIKASI      : Maksimal mahasiswa tersebut adalah tahun {tahun_batas}")
        print("======================================")

# 2. Kelas Anak: Sarjana (S1)
class Sarjana(Mahasiswa):
    def __init__(self, nama):
        super().__init__(nama)

        self.maks_kuliah = 7  # 14 semester = 7 tahun

        # Panggil fungsi generate NIM dengan kode program "1"
        self.generate_nim(kode_program="1")

# 3. Kelas Anak: Pascasarjana (S2/S3)
class Pascasarjana(Mahasiswa):
    def __init__(self, nama):
        super().__init__(nama)

        self.maks_kuliah = 4  # 8 semester = 4 tahun

        # Panggil fungsi generate NIM dengan kode program "2"
        self.generate_nim(kode_program="2")
# ==========================================================
# ALUR INPUT PENGGUNA (STUDI KASUS)
# ==========================================================

def main():
    print("==========================================")
    print("     SISTEM PENDAFTARAN MAHASISWA BARU    ")
    print("==========================================")

    print("Pilih Program Pendidikan:")
    print("1. Program Sarjana")
    print("2. Program Pascasarjana")

    pilihan = input("Masukkan pilihan (1/2): ")

    if pilihan not in ["1", "2"]:
        print("\nPilihan tidak valid! Program dihentikan.")
        return

    input_nama = input("Masukkan Nama Mahasiswa: ")

    # Proses Polimorfisme & Inheritance berdasarkan pilihan user
    if pilihan == "1":
        mahasiswa_baru = Sarjana(input_nama)
    else:
        mahasiswa_baru = Pascasarjana(input_nama)

    # Menampilkan hasil cetak data dan notifikasi tahun kelulusan
    mahasiswa_baru.tampilkan_info()

if __name__ == "__main__":
    main()