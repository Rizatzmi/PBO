import random
from datetime import date

class Anggota:
    def __init__(self, nomor_anggota, nama, alamat, no_hp):
        self.nomor_anggota = nomor_anggota
        self.nama = nama
        self.alamat = alamat
        self.no_hp = no_hp
        self.daftar_buku = []

    def pinjam_buku(self, item_buku):
        self.daftar_buku.append(item_buku)


class Buku:
    def __init__(self, kode_buku, judul_buku, penulis, tahun_terbit):
        self.kode_buku = kode_buku
        self.judul_buku = judul_buku
        self.penulis = penulis
        self.tahun_terbit = tahun_terbit


# [PERUBAHAN] Ditambah atribut nomor_transaksi, tanggal_pinjam, tanggal_kembali
# agar bisa mendukung fitur Menu 3 (output nomor transaksi & tanggal pinjam),
# Menu 4 (tanggal kembali), dan Menu 7 (riwayat peminjaman).
class StatusBuku:
    def __init__(self, buku, nomor_transaksi, tanggal_pinjam, anggota):
        self.buku = buku
        self.status = "Dipinjam"        # "Dipinjam" atau "Tersedia"
        self.nomor_transaksi = nomor_transaksi
        self.tanggal_pinjam = tanggal_pinjam
        self.tanggal_kembali = None
        self.anggota = anggota          # referensi ke objek Anggota peminjam


class SistemPerpus:
    def __init__(self):
        self.data_anggota = {}          # key: nomor_anggota
        self.data_buku = {}             # key: kode_buku → objek Buku
        self.status_buku = {}           # key: kode_buku → objek StatusBuku (aktif)
        self.riwayat_peminjaman = []    # list semua StatusBuku (termasuk sudah kembali)
        self.counter_transaksi = 1      # untuk nomor transaksi urut

    # ------------------------------------------------------------------ #
    #  HELPER INPUT
    # ------------------------------------------------------------------ #

    def input_angka(self, pesan):
        """Input integer positif (untuk tahun terbit, nomor anggota, dsb.)"""
        while True:
            try:
                nilai = int(input(pesan))
                if nilai <= 0:
                    print("Input harus lebih dari 0.")
                else:
                    return nilai
            except ValueError:
                print("Input harus berupa angka.")

    # [PERUBAHAN] Validasi no HP dipisah dari input_angka biasa karena nomor HP
    # bisa sangat panjang dan harus diawali 62, sehingga lebih tepat sebagai string.
    def input_no_hp(self, pesan):
        """Input nomor HP: hanya digit, diawali 62."""
        while True:
            nilai = input(pesan).strip()
            if not nilai.isdigit():
                print("No HP harus berupa angka.")
            elif not nilai.startswith("62"):
                print("No HP harus diawali dengan 62.")
            else:
                return nilai

    # ------------------------------------------------------------------ #
    #  HELPER CARI DATA
    # ------------------------------------------------------------------ #

    def cari_anggota(self, nomor_anggota):
        return self.data_anggota.get(nomor_anggota)

    def cari_buku(self, kode_buku):
        return self.data_buku.get(kode_buku)

    # ------------------------------------------------------------------ #
    #  MENU 1 – TAMBAH DATA BUKU
    # ------------------------------------------------------------------ #

    def tambah_buku(self):
        print("\n=== TAMBAHKAN BUKU ===")

        while True:
            kode_buku = input("Masukkan Kode Buku  : ").strip().upper()
            if kode_buku in self.data_buku:
                # [SESUAI SPESIFIKASI] Notif kode sama, kembali ke input kode buku
                print("Kode buku sudah terdaftar. Masukkan kode yang berbeda.")
            else:
                break

        judul_buku   = input("Masukkan Judul Buku  : ")
        penulis      = input("Masukkan Penulis     : ")
        tahun_terbit = self.input_angka("Masukkan Tahun Terbit: ")

        buku = Buku(kode_buku, judul_buku, penulis, tahun_terbit)
        self.data_buku[kode_buku] = buku

        print("\nData Buku berhasil ditambahkan.")
        print(f"Kode Buku    : {kode_buku}")
        print(f"Judul Buku   : {judul_buku}")
        print(f"Penulis      : {penulis}")
        print(f"Tahun Terbit : {tahun_terbit}")

    # ------------------------------------------------------------------ #
    #  MENU 2 – TAMBAH DATA ANGGOTA
    # ------------------------------------------------------------------ #

    def tambah_anggota(self):
        print("\n=== TAMBAHKAN ANGGOTA ===")

        # Pastikan nomor anggota unik
        while True:
            nomor_anggota = random.randint(1, 99999)
            if nomor_anggota not in self.data_anggota:
                break

        nama   = input("Masukkan Nama   : ")
        alamat = input("Masukkan Alamat : ")
        # [PERUBAHAN] Menggunakan input_no_hp() bukan input_angka()
        no_hp  = self.input_no_hp("Masukkan No HP (awali 62): ")

        anggota = Anggota(nomor_anggota, nama, alamat, no_hp)
        self.data_anggota[nomor_anggota] = anggota

        print("\nData Anggota berhasil ditambahkan.")
        print(f"Nomor Anggota : {nomor_anggota}")
        print(f"Nama          : {nama}")
        print(f"Alamat        : {alamat}")
        print(f"No HP         : {no_hp}")

    # ------------------------------------------------------------------ #
    #  MENU 3 – PINJAM BUKU
    # ------------------------------------------------------------------ #

    def pinjam_buku(self):
        print("\n=== PINJAM BUKU ===")

        if not self.data_anggota:
            print("Belum ada data anggota.")
            return
        if not self.data_buku:
            print("Belum ada data buku.")
            return

        # Input & validasi nomor anggota
        nomor_anggota = self.input_angka("Masukkan Nomor Anggota: ")
        anggota = self.cari_anggota(nomor_anggota)
        if anggota is None:
            print("Anggota tidak ditemukan.")
            return

        print("\nData Anggota")
        print(f"Nama   : {anggota.nama}")
        print(f"Alamat : {anggota.alamat}")
        print(f"No HP  : {anggota.no_hp}")

        # Input & validasi kode buku (loop sampai kode ditemukan)
        # [PERUBAHAN] Diganti dari input_angka() ke input().upper()
        # karena kode buku adalah string (misal: "BK001"), bukan integer.
        while True:
            kode_buku = input("\nMasukkan Kode Buku: ").strip().upper()
            buku = self.cari_buku(kode_buku)
            if buku is None:
                # [SESUAI SPESIFIKASI] Notif & kembali input kode buku
                print("Kode tidak tersedia. Masukkan kode buku yang benar.")
                continue

            # Cek apakah buku sedang dipinjam
            if kode_buku in self.status_buku and self.status_buku[kode_buku].status == "Dipinjam":
                print("Buku ini sedang dipinjam oleh anggota lain dan tidak bisa dipinjam.")
                return

            break   # kode ada dan status tersedia → lanjut

        # Buat transaksi
        nomor_transaksi = f"TRX{self.counter_transaksi:04d}"
        self.counter_transaksi += 1
        tanggal_pinjam = date.today()

        item_buku = StatusBuku(buku, nomor_transaksi, tanggal_pinjam, anggota)
        self.status_buku[kode_buku] = item_buku
        # [PERUBAHAN] Typo diperbaiki: pinjem_buku → pinjam_buku
        anggota.pinjam_buku(item_buku)
        self.riwayat_peminjaman.append(item_buku)

        print("\n--- Peminjaman Berhasil ---")
        print(f"Nomor Transaksi : {nomor_transaksi}")
        print(f"Nama Anggota    : {anggota.nama}")
        print(f"Judul Buku      : {buku.judul_buku}")
        print(f"Tanggal Pinjam  : {tanggal_pinjam.strftime('%d-%m-%Y')}")

    # ------------------------------------------------------------------ #
    #  MENU 4 – KEMBALIKAN BUKU
    # ------------------------------------------------------------------ #

    def kembalikan_buku(self):
        print("\n=== KEMBALIKAN BUKU ===")

        if not self.status_buku:
            print("Tidak ada buku yang sedang dipinjam.")
            return

        # Input & validasi kode buku (loop sampai kode ditemukan)
        while True:
            kode_buku = input("Masukkan Kode Buku: ").strip().upper()
            if kode_buku not in self.data_buku:
                # [SESUAI SPESIFIKASI] Notif kode tidak tersedia, kembali input
                print("Kode tidak tersedia. Masukkan kode buku yang benar.")
                continue

            if kode_buku not in self.status_buku or self.status_buku[kode_buku].status != "Dipinjam":
                # [SESUAI SPESIFIKASI] Buku ada tapi tidak sedang dipinjam
                print("Buku ini tidak sedang dipinjam.")
                return

            break   # valid dan sedang dipinjam

        item_buku = self.status_buku[kode_buku]
        tanggal_kembali = date.today()
        item_buku.status = "Tersedia"
        item_buku.tanggal_kembali = tanggal_kembali

        # Hapus dari status aktif (buku sudah tersedia kembali)
        del self.status_buku[kode_buku]

        print("\n--- Pengembalian Berhasil ---")
        print(f"Nomor Transaksi  : {item_buku.nomor_transaksi}")
        print(f"Nama Anggota     : {item_buku.anggota.nama}")
        print(f"Judul Buku       : {item_buku.buku.judul_buku}")
        print(f"Tanggal Kembali  : {tanggal_kembali.strftime('%d-%m-%Y')}")

    # ------------------------------------------------------------------ #
    #  MENU 5 – INFO ANGGOTA
    # ------------------------------------------------------------------ #

    def info_anggota(self):
        print("\n=== INFO ANGGOTA ===")

        if not self.data_anggota:
            print("Belum ada data anggota.")
            return

        # Input & validasi nomor anggota (loop sampai ditemukan)
        while True:
            nomor_anggota = self.input_angka("Masukkan Nomor Anggota: ")
            anggota = self.cari_anggota(nomor_anggota)
            if anggota is None:
                # [SESUAI SPESIFIKASI] Notif & kembali ke input nomor anggota
                print("Anggota tidak ditemukan. Coba lagi.")
                continue
            break

        print(f"\nNomor Anggota : {anggota.nomor_anggota}")
        print(f"Nama          : {anggota.nama}")
        print(f"Alamat        : {anggota.alamat}")
        print(f"No HP         : {anggota.no_hp}")

        # Filter buku yang masih/pernah dipinjam anggota ini
        buku_dipinjam = anggota.daftar_buku

        if not buku_dipinjam:
            # [SESUAI SPESIFIKASI] Notif jika belum pernah pinjam
            print("\nTidak ada buku yang dipinjam.")
        else:
            # [SESUAI SPESIFIKASI] Tampilan mendatar: No.urut, Kode Buku, Judul Buku, Status
            print("\nDaftar Pinjaman:")
            print("-" * 70)
            print(f"{'No':<5} {'Kode Buku':<15} {'Judul Buku':<35} {'Status':<10}")
            print("-" * 70)
            for i, item in enumerate(buku_dipinjam, start=1):
                print(
                    f"{i:<5} "
                    f"{item.buku.kode_buku:<15} "
                    f"{item.buku.judul_buku:<35} "
                    f"{item.status:<10}"
                )
            print("-" * 70)

    # ------------------------------------------------------------------ #
    #  MENU 6 – DAFTAR BUKU
    # ------------------------------------------------------------------ #

    def tampilkan_buku(self):
        print("\n=== DAFTAR BUKU ===")

        if not self.data_buku:
            # [SESUAI SPESIFIKASI] Notif jika belum ada data buku
            print("Belum ada data buku.")
            return

        # [SESUAI SPESIFIKASI] Mendatar: No urut, Kode Buku, Judul, Penulis, Tahun, Status
        print("-" * 95)
        print(f"{'No':<5} {'Kode Buku':<12} {'Judul Buku':<35} {'Penulis':<15} {'Tahun':<8} {'Status':<10}")
        print("-" * 95)
        for i, buku in enumerate(self.data_buku.values(), start=1):
            # Tentukan status: cek apakah kode buku ada di status aktif
            if buku.kode_buku in self.status_buku and self.status_buku[buku.kode_buku].status == "Dipinjam":
                status = "Dipinjam"
            else:
                status = "Tersedia"
            print(
                f"{i:<5} "
                f"{buku.kode_buku:<12} "
                f"{buku.judul_buku:<35} "
                f"{buku.penulis:<15} "
                f"{buku.tahun_terbit:<8} "
                f"{status:<10}"
            )
        print("-" * 95)

    # ------------------------------------------------------------------ #
    #  MENU 7 – RIWAYAT PEMINJAMAN
    # ------------------------------------------------------------------ #

    def riwayat_peminjaman_menu(self):
        print("\n=== RIWAYAT PEMINJAMAN ===")

        if not self.riwayat_peminjaman:
            print("Belum ada riwayat peminjaman.")
            return

        # [SESUAI SPESIFIKASI] Header: No, No Transaksi, Tgl Pinjam, Tgl Kembali,
        # Nama Anggota, Kode Buku, Judul, Status
        print("-" * 115)
        print(
            f"{'No':<4} {'No Transaksi':<12} {'Tgl Pinjam':<13} {'Tgl Kembali':<13} "
            f"{'Nama Anggota':<20} {'Kode Buku':<12} {'Judul Buku':<25} {'Status':<10}"
        )
        print("-" * 115)
        for i, item in enumerate(self.riwayat_peminjaman, start=1):
            tgl_kembali = item.tanggal_kembali.strftime('%d-%m-%Y') if item.tanggal_kembali else "-"
            print(
                f"{i:<4} "
                f"{item.nomor_transaksi:<12} "
                f"{item.tanggal_pinjam.strftime('%d-%m-%Y'):<13} "
                f"{tgl_kembali:<13} "
                f"{item.anggota.nama:<20} "
                f"{item.buku.kode_buku:<12} "
                f"{item.buku.judul_buku:<25} "
                f"{item.status:<10}"
            )
        print("-" * 115)

    # ------------------------------------------------------------------ #
    #  MENU UTAMA
    # ------------------------------------------------------------------ #

    def tampilkan_menu(self):
        print("\n====================================")
        print("        SISTEM PERPUSTAKAAN 2")
        print("====================================")
        print("1. Tambahkan Data Buku")
        print("2. Tambahkan Data Anggota")
        print("3. Pinjam Buku")
        print("4. Kembalikan Buku")
        print("5. Info Anggota")
        print("6. Daftar Buku")
        print("7. Riwayat Peminjaman")
        print("8. Keluar")

    def jalankan(self):
        while True:
            self.tampilkan_menu()
            pilihan = input("Pilih menu [1-8]: ")

            if pilihan == "1":
                self.tambah_buku()
            elif pilihan == "2":
                self.tambah_anggota()
            elif pilihan == "3":
                self.pinjam_buku()
            elif pilihan == "4":
                self.kembalikan_buku()
            elif pilihan == "5":
                self.info_anggota()
            elif pilihan == "6":
                self.tampilkan_buku()
            elif pilihan == "7":
                self.riwayat_peminjaman_menu()
            elif pilihan == "8":
                print("Program selesai. Terima kasih.")
                break
            else:
                print("Pilihan tidak valid. Silakan pilih menu 1 sampai 8.")


program = SistemPerpus()
program.jalankan()