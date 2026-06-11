from abc import ABC, abstractmethod

class Mahasiswa(ABC):

    def __init__(self, nama, nim, prodi):
        self.__nama = nama      # atribut private dengan __ (enkapsulasi)
        self.__nim = nim
        self.__prodi = prodi

    # enkapsulasi dengan getter dan setter menggunakan decorator
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
    def nim(self, input):
        if len(input) != 9:
            raise ValueError("NIM Institut Asia harus 9 digit")
        self.__nim = input

    @property
    def prodi(self):
        return self.__prodi

    @prodi.setter
    def prodi(self, input):
        self.__prodi = input

    @abstractmethod
    def info_mahasiswa(self):
        pass

    @abstractmethod
    def hitung_ipk(self):
        pass

    @abstractmethod
    def status_aktif(self):
        pass

# Subclass 1: MahasiswaReguler
class MahasiswaReguler(Mahasiswa):

    def __init__(self, nama, nim, prodi, ipk):
        super().__init__(nama, nim, prodi)
        self._ipk = ipk

    def info_mahasiswa(self):
        return f"Reguler: NIM: {self.nim}, Nama : {self.nama}, Program Studi : {self.prodi}"

    def hitung_ipk(self):
        print(f"IPK sekarang : {self._ipk}")

    def status_aktif(self):
        return "Aktif"


# Subclass 2: MahasiswaKaryawan
class MahasiswaKaryawan(Mahasiswa):

    def __init__(self, nama, nim, prodi, ipk, jam_kerja):
        super().__init__(nama, nim, prodi)
        self._ipk = ipk
        self._jam_kerja = jam_kerja  # jam kerja per minggu

    def info_mahasiswa(self):
        return f"Karyawan: NIM: {self.nim}, Nama : {self.nama}, Program Studi : {self.prodi}, Jam Kerja: {self._jam_kerja}"

    def hitung_ipk(self):
        # Misal mahasiswa karyawan biasanya dapat beban belajar berkurang
        faktor = 1 if self._jam_kerja > 20 else 0.9
        print(f"IPK sekarang : {self._ipk * faktor}")

    def status_aktif(self):
        return "Aktif"
    
# Subclass 3: MahasiswaRPL
class MahasiswaRPL(Mahasiswa):

    def __init__(self, nama, nim, prodi, IPKasses, IPKasia):
        super().__init__(nama, nim, prodi)
        self._IPKasses = IPKasses
        self._IPKasia = IPKasia

    def info_mahasiswa(self):
        return (
            f"Rekognisi Pembelajaran Lampau : NIM: {self.nim}, Nama : {self.nama}, "
            f"Program Studi : {self.prodi}, IPK hasil Assesmen : {self._IPKasses}"
            f"IPK di Asia : {self._IPKasia}"
        )

    def hitung_ipk(self):
        # Bisa ada aturan khusus IPK untuk mahasiswa RPL
        self._ipk = (self._IPKasses + self._IPKasia) / 2
        print(f"IPK sekarang : {round(self._ipk, 2)}")

    def status_aktif(self):
        return "Aktif"


# Contoh penggunaan
# m1 = MahasiswaReguler("Budi", "12345678", "Teknik Informatika", 3.75)
# m2 = MahasiswaKaryawan("Ani", "87654321", "Sistem Informasi", 3.4, 25)
# m3 = MahasiswaRPL("John", "11223344", "Teknik Elektro", 3.6, 3.12)

# print(m1.info_mahasiswa())
# m1.hitung_ipk()
# print(m1.status_aktif())

# print(m2.info_mahasiswa())
# m2.hitung_ipk()
# print(m2.status_aktif())

# print(m3.info_mahasiswa())
# m3.hitung_ipk()
# print(m3.status_aktif())

m1 = MahasiswaReguler("Budi", "1234567890", "Teknik Informatika", 3.75)
m1.nim = "987654321"