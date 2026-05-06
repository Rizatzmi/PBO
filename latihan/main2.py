import random
from datetime import datetime


class Transaksi:
    def __init__(self, keterangan, debet=0, kredit=0, saldo_akhir=0):
        self.tanggal = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.keterangan = keterangan
        self.debet = debet
        self.kredit = kredit
        self.saldo_akhir = saldo_akhir


class Nasabah:
    def __init__(self, nama, nik, alamat, nama_ibu, saldo_awal):
        self.nama = nama
        self.nik = nik
        self.alamat = alamat
        self.nama_ibu = nama_ibu
        self.saldo = saldo_awal
        self.norek = self._generate_norek()
        self.riwayat = []
        self.riwayat.append(Transaksi("Setoran Awal", kredit=saldo_awal, saldo_akhir=saldo_awal))

    def _generate_norek(self):
        return str(random.randint(10000, 99999))

    def setor(self, jumlah):
        self.saldo += jumlah
        self.riwayat.append(Transaksi("Setoran Tunai", kredit=jumlah, saldo_akhir=self.saldo))

    def tarik(self, jumlah):
        if jumlah > self.saldo:
            return False
        self.saldo -= jumlah
        self.riwayat.append(Transaksi("Penarikan Tunai", debet=jumlah, saldo_akhir=self.saldo))
        return True

    def transfer_keluar(self, jumlah, bank_tujuan, norek_tujuan):
        if jumlah > self.saldo:
            return False
        self.saldo -= jumlah
        ket = f"Transfer ke {bank_tujuan} - {norek_tujuan}"
        self.riwayat.append(Transaksi(ket, debet=jumlah, saldo_akhir=self.saldo))
        return True


class Bank:
    def __init__(self, nama_bank="MyBank"):
        self.nama_bank = nama_bank
        self.nasabah = {}  # norek -> Nasabah

    def tambah_nasabah(self):
        print("\n" + "="*45)
        print("        PENDAFTARAN NASABAH BARU")
        print("="*45)
        nama     = input("Nama Lengkap     : ").strip()
        nik      = input("NIK              : ").strip()
        alamat   = input("Alamat           : ").strip()
        nama_ibu = input("Nama Ibu Kandung : ").strip()
        while True:
            try:
                saldo_awal = float(input("Saldo Awal (Rp)  : "))
                if saldo_awal < 0:
                    print("  [!] Saldo awal tidak boleh negatif.")
                    continue
                break
            except ValueError:
                print("  [!] Masukkan angka yang valid.")

        nasabah = Nasabah(nama, nik, alamat, nama_ibu, saldo_awal)
        # Pastikan norek unik
        while nasabah.norek in self.nasabah:
            nasabah.norek = nasabah._generate_norek()
        self.nasabah[nasabah.norek] = nasabah

        print("\n  [✓] Nasabah berhasil didaftarkan!")
        print(f"  Nomor Rekening Anda : {nasabah.norek}")

    def _cari_nasabah(self, prompt="Nomor Rekening : "):
        norek = input(prompt).strip()
        nasabah = self.nasabah.get(norek)
        if not nasabah:
            print("  [!] Nomor rekening tidak ditemukan.")
        return nasabah

    def setor_tunai(self):
        print("\n" + "="*45)
        print("              SETOR TUNAI")
        print("="*45)
        nasabah = self._cari_nasabah()
        if not nasabah:
            return
        print(f"  Nama        : {nasabah.nama}")
        print(f"  Saldo       : Rp {nasabah.saldo:,.0f}")
        while True:
            try:
                jumlah = float(input("Jumlah Setoran (Rp) : "))
                if jumlah <= 0:
                    print("  [!] Jumlah harus lebih dari 0.")
                    continue
                break
            except ValueError:
                print("  [!] Masukkan angka yang valid.")
        nasabah.setor(jumlah)
        print(f"\n  [✓] Setoran berhasil.")
        print(f"  Saldo Akhir : Rp {nasabah.saldo:,.0f}")

    def tarik_tunai(self):
        print("\n" + "="*45)
        print("              TARIK TUNAI")
        print("="*45)
        nasabah = self._cari_nasabah()
        if not nasabah:
            return
        print(f"  Nama        : {nasabah.nama}")
        print(f"  Saldo       : Rp {nasabah.saldo:,.0f}")
        while True:
            try:
                jumlah = float(input("Jumlah Penarikan (Rp) : "))
                if jumlah <= 0:
                    print("  [!] Jumlah harus lebih dari 0.")
                    continue
                if jumlah > nasabah.saldo:
                    print(f"  [!] Saldo tidak mencukupi. Saldo Anda: Rp {nasabah.saldo:,.0f}")
                    continue
                break
            except ValueError:
                print("  [!] Masukkan angka yang valid.")
        nasabah.tarik(jumlah)
        print(f"\n  [✓] Penarikan berhasil.")
        print(f"  Saldo Akhir : Rp {nasabah.saldo:,.0f}")

    def transfer(self):
        print("\n" + "="*45)
        print("               TRANSFER")
        print("="*45)
        nasabah = self._cari_nasabah()
        if not nasabah:
            return
        print(f"  Nama        : {nasabah.nama}")
        print(f"  Saldo       : Rp {nasabah.saldo:,.0f}")
        bank_tujuan  = input("Bank Tujuan        : ").strip()
        norek_tujuan = input("Nomor Rek Tujuan   : ").strip()
        while True:
            try:
                jumlah = float(input("Jumlah Transfer (Rp) : "))
                if jumlah <= 0:
                    print("  [!] Jumlah harus lebih dari 0.")
                    continue
                if jumlah > nasabah.saldo:
                    print(f"  [!] Saldo tidak mencukupi. Saldo Anda: Rp {nasabah.saldo:,.0f}")
                    continue
                break
            except ValueError:
                print("  [!] Masukkan angka yang valid.")
        nasabah.transfer_keluar(jumlah, bank_tujuan, norek_tujuan)
        print(f"\n  [✓] Transfer berhasil.")
        print(f"  Saldo Akhir : Rp {nasabah.saldo:,.0f}")

    def info_rekening(self):
        print("\n" + "="*65)
        print("                  INFO REKENING")
        print("="*65)
        nasabah = self._cari_nasabah()
        if not nasabah:
            return
        print(f"  Nama    : {nasabah.nama}")
        print(f"  Alamat  : {nasabah.alamat}")
        print(f"  No. Rek : {nasabah.norek}")
        print("-"*65)
        header = f"{'No':>3}  {'Tanggal':<20} {'Keterangan':<28} {'Debet':>10} {'Kredit':>10}"
        print(header)
        print("-"*65)
        for i, t in enumerate(nasabah.riwayat, 1):
            debet  = f"{t.debet:,.0f}"  if t.debet  > 0 else "-"
            kredit = f"{t.kredit:,.0f}" if t.kredit > 0 else "-"
            print(f"  {i:>2}  {t.tanggal:<20} {t.keterangan:<28} {debet:>10} {kredit:>10}")
        print("-"*65)
        print(f"  {'Saldo Akhir':>52} : Rp {nasabah.saldo:,.0f}")
        print("="*65)

    def menu_utama(self):
        while True:
            print("\n" + "="*45)
            print(f"     SELAMAT DATANG DI {self.nama_bank.upper()}")
            print("="*45)
            print("  1. Tambah Data Nasabah")
            print("  2. Setor Tunai")
            print("  3. Tarik Tunai")
            print("  4. Transfer")
            print("  5. Info Rekening")
            print("  6. Keluar Program")
            print("-"*45)
            pilihan = input("  Pilih Menu [1-6] : ").strip()

            if pilihan == "1":
                self.tambah_nasabah()
            elif pilihan == "2":
                self.setor_tunai()
            elif pilihan == "3":
                self.tarik_tunai()
            elif pilihan == "4":
                self.transfer()
            elif pilihan == "5":
                self.info_rekening()
            elif pilihan == "6":
                print("\n  Terima kasih telah menggunakan layanan kami.")
                print("  Sampai jumpa!\n")
                break
            else:
                print("  [!] Pilihan tidak valid. Silakan pilih 1-6.")


if __name__ == "__main__":
    bank = Bank("MyBank")
    bank.menu_utama()