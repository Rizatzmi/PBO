class mhs():
    pass

saya=mhs()
teman1=mhs()
teman2=mhs()

saya.nim="2121212"
saya.nama="Dwi Putra"
saya.gender="Laki-laki"
saya.jurusan="Teknik Informatika"

teman1.nim="2121213"
teman1.nama="Dwi Putri"
teman1.gender="Perempuan"
teman1.jurusan="DKV"

teman2.nim="2121214"
teman2.nama="Andini"
teman2.gender="Perempuan"
teman2.jurusan="PBM"

print(saya)
print(saya.__dict__)
print("Nama teman saya adalah", teman1.nama, " dengan NIM ", teman1.nim, " dan jurusan ", teman1.jurusan, "dan", "Nama teman saya adalah", teman2.nama, " dengan NIM ", teman2.nim, " dan jurusan ", teman2.jurusan)