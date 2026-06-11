from abstract_mhs import MahasiswaReguler, MahasiswaKaryawan, MahasiswaRPL

def main():
    print("=" * 40)
    print("SISTEM DATA MAHASISWA")
    print("=" * 40)
    print("Pilih Jenis Mahasiswa:")
    print("1. Mahasiswa Reguler")
    print("2. Mahasiswa Karyawan")
    print("3. Mahasiswa RPL")

    pilihan = input("Masukkan pilihan (1-3): ")

    nama = input("Nama  : ")
    nim = input("NIM   : ")
    prodi = input("Prodi : ")

    if pilihan == "1":
        ipk = float(input("Masukkan IPK: "))

        mhs = MahasiswaReguler(
            nama=nama,
            nim=nim,
            prodi=prodi,
            ipk=ipk
        )

        mhs.nim = input("Masukkan NIM baru (9 digit): ") 


    elif pilihan == "2":
        ipk = float(input("Masukkan IPK: "))
        jam_kerja = int(input("Jam Kerja per Minggu: "))

        mhs = MahasiswaKaryawan(
            nama=nama,
            nim=nim,
            prodi=prodi,
            ipk=ipk,
            jam_kerja=jam_kerja
        )

    elif pilihan == "3":
        ipk_asses = float(input("IPK Hasil Assesmen: "))
        ipk_asia = float(input("IPK di Asia: "))

        mhs = MahasiswaRPL(
            nama=nama,
            nim=nim,
            prodi=prodi,
            IPKasses=ipk_asses,
            IPKasia=ipk_asia
        )

    else:
        print("Pilihan tidak valid!")
        return

    print("\n" + "=" * 40)
    print("DATA MAHASISWA")
    print("=" * 40)

    print(mhs.info_mahasiswa())
    mhs.hitung_ipk()
    print("Status :", mhs.status_aktif())


if __name__ == "__main__":
    main()