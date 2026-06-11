class Buku:

    def __init__(self, judul, halaman):
        self.judul = judul
        self.halaman = halaman

    def __str__(self):
        return f"Buku: {self.judul} ({self.halaman} halaman)"

    def __len__(self):
        return self.halaman

    def __add__(self, other):
        return self.halaman + other.halaman

    def __eq__(self, other):
        return self.halaman == other.halaman


# Pemakaian
b1 = Buku("Python Dasar", 300)
b2 = Buku("Python Lanjut", 400)
b3 = Buku("Python Dasar", 300)

print(str(b1))      # __str__ -> Buku: Python Dasar (300 halaman)
print(len(b1))      # __len__ -> ambil jumlah halaman : 300
print(b1 + b2)      # __add__ -> jumlah halaman b1 + jumlah halaman b2 = 700
print(b1 == b3)     # __eq__ -> True -> membandingkan nilai jumlah halaman b1 dgn b3