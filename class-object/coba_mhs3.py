class mhs():
    def __init__(self, nomorinduk, nama, gender, jurusan):
        self.nim = nomorinduk
        self.nama = nama
        self.gender = gender
        self.jurusan = jurusan

saya=mhs("2121212", "Dwi Putra", "Laki-laki", "Teknik Informatika")
teman1=mhs("2121213", "Dwi Putri", "Perempuan", "DKV")
teman2=mhs("2121214", "Andini", "Perempuan", "PBM")
print("aku seorang", saya.gender, "bernama", saya.nama, "kuliah di asia jurusan", saya.jurusan, "punya teman di prodi", teman1.jurusan, "namanya", teman1.nama)
print("aku juga punya teman", teman2.gender, "di prodi", teman2.jurusan, "namanya", teman2.nama)
print("NIM kami bertiga adalah :" , saya.nim, "," , teman1.nim, "," , teman2.nim)