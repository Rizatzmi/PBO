"""
=============================================================
  FILE: music_classes.py
  Deskripsi: Deklarasi OOP - Kelas untuk Aplikasi Musik
  Pilar OOP: Enkapsulasi, Inheritance, Abstraction, Polymorphism
=============================================================
"""

from abc import ABC, abstractmethod
import random


# ============================================================
# ABSTRACTION -- Abstract Base Class
# ============================================================

class Media(ABC):
    """
    Abstract class sebagai kontrak dasar item media.
    ABSTRACTION: method get_info() dan __str__() wajib
    diimplementasikan oleh subclass.
    """

    @abstractmethod
    def get_info(self) -> str:
        pass

    @abstractmethod
    def get_duration(self) -> int:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass


# ============================================================
# CLASS: Lagu  (Enkapsulasi + Inheritance)
# ============================================================

class Lagu(Media):
    """
    Representasi sebuah lagu.
    ENKAPSULASI : atribut privat diakses via getter/setter.
    INHERITANCE : mewarisi Media dan mengimplementasikan
                  semua method abstraknya.
    """

    @staticmethod
    def parse_durasi(durasi_str: str) -> int:
        """
        Parse format MM:SS menjadi total detik.
        Raise ValueError jika format tidak valid.
        """
        bagian = durasi_str.strip().split(":")
        if len(bagian) != 2:
            raise ValueError("Format harus MM:SS")
        menit_str, detik_str = bagian
        if not menit_str.isdigit() or not detik_str.isdigit():
            raise ValueError("Menit dan detik harus angka")
        menit = int(menit_str)
        detik = int(detik_str)
        if detik < 0 or detik > 59:
            raise ValueError("Detik harus antara 00 dan 59")
        if menit < 0:
            raise ValueError("Menit tidak boleh negatif")
        return menit * 60 + detik

    def __init__(self, judul: str, artis: str, durasi: int, genre: str = "Unknown"):
        self.__judul      = judul
        self.__artis      = artis
        self.__durasi     = durasi
        self.__genre      = genre
        self.__play_count = 0

    # -- Getter --
    @property
    def judul(self) -> str:
        return self.__judul

    @property
    def artis(self) -> str:
        return self.__artis

    @property
    def genre(self) -> str:
        return self.__genre

    @property
    def play_count(self) -> int:
        return self.__play_count

    # -- Setter dengan validasi (Enkapsulasi) --
    @judul.setter
    def judul(self, value: str):
        if not value.strip():
            raise ValueError("Judul tidak boleh kosong.")
        self.__judul = value.strip()

    @artis.setter
    def artis(self, value: str):
        if not value.strip():
            raise ValueError("Nama artis tidak boleh kosong.")
        self.__artis = value.strip()

    @genre.setter
    def genre(self, value: str):
        self.__genre = value.strip() if value.strip() else "Unknown"

    def set_durasi(self, durasi: int):
        if durasi <= 0:
            raise ValueError("Durasi harus lebih dari 0.")
        self.__durasi = durasi

    # -- Method --
    def increment_play(self):
        self.__play_count += 1

    def format_durasi(self) -> str:
        return f"{self.__durasi // 60:02d}:{self.__durasi % 60:02d}"

    # -- Implementasi abstract method --
    def get_duration(self) -> int:
        return self.__durasi

    def get_info(self) -> str:
        return (f"{self.__judul} | Artis: {self.__artis}"
                f" | Genre: {self.__genre} | Durasi: {self.format_durasi()}"
                f" | Diputar: {self.__play_count}x")

    def __str__(self) -> str:
        return f"{self.__judul} - {self.__artis} ({self.format_durasi()})"


# ============================================================
# CLASS: Playlist  (Enkapsulasi + Polymorphism via Media)
# ============================================================

class Playlist:
    """
    Kumpulan objek Lagu (turunan Media).
    ENKAPSULASI : daftar lagu privat, diubah lewat method.
    POLYMORPHISM: menerima semua turunan Media.
    """

    def __init__(self, nama: str):
        self.__nama        = nama
        self.__lagu_list: list[Media] = []
        self.__shuffled:  list[Media] = []
        self.__is_shuffled = False

    # -- Getter --
    @property
    def nama(self) -> str:
        return self.__nama

    @property
    def is_shuffled(self) -> bool:
        return self.__is_shuffled

    @property
    def total_lagu(self) -> int:
        return len(self.__lagu_list)

    @property
    def total_durasi(self) -> str:
        total = sum(item.get_duration() for item in self.__lagu_list)
        return f"{total // 60:02d}:{total % 60:02d}"

    # -- Setter --
    @nama.setter
    def nama(self, value: str):
        if not value.strip():
            raise ValueError("Nama playlist tidak boleh kosong.")
        self.__nama = value.strip()

    # -- Method --
    def tambah_lagu(self, lagu: Media):
        if not isinstance(lagu, Media):
            raise TypeError("Item harus turunan dari Media.")
        self.__lagu_list.append(lagu)

    def hapus_lagu(self, judul: str) -> bool:
        for item in self.__lagu_list:
            if item.judul.lower() == judul.lower():
                self.__lagu_list.remove(item)
                self.__is_shuffled = False
                return True
        return False

    def shuffle(self):
        if not self.__lagu_list:
            return False
        self.__shuffled = self.__lagu_list.copy()
        random.shuffle(self.__shuffled)
        self.__is_shuffled = True
        return True

    def unshuffle(self):
        self.__shuffled    = []
        self.__is_shuffled = False

    def get_active_list(self) -> list[Media]:
        return self.__shuffled if self.__is_shuffled else self.__lagu_list

    def get_item(self, index: int):
        active = self.get_active_list()
        return active[index] if 0 <= index < len(active) else None

    def __str__(self) -> str:
        return f"Playlist '{self.__nama}' ({self.total_lagu} lagu)"


# ============================================================
# CLASS: Player  (Enkapsulasi + Polymorphism)
# ============================================================

class Player:
    """
    Pemutar lagu dari sebuah Playlist.
    ENKAPSULASI : status internal (status, index) privat.
    POLYMORPHISM: play() bekerja dengan semua turunan Media.
    """

    PLAYING = "PLAYING"
    PAUSED  = "PAUSED"
    STOPPED = "STOPPED"

    def __init__(self):
        self.__status   = self.STOPPED
        self.__playlist = None
        self.__index    = -1
        self.__current  = None

    # -- Getter --
    @property
    def status(self) -> str:
        return self.__status

    @property
    def current(self):
        return self.__current

    @property
    def current_index(self) -> int:
        return self.__index

    @property
    def playlist(self):
        return self.__playlist

    # -- Method --
    def load(self, playlist: Playlist):
        self.__playlist = playlist
        self.__index    = -1
        self.__status   = self.STOPPED
        self.__current  = None

    def play(self):
        if self.__playlist is None:
            return False, "Tidak ada playlist yang dimuat."
        if self.__status == self.PAUSED and self.__current:
            self.__status = self.PLAYING
            return True, f"Lanjut: {self.__current}"
        if self.__index < 0:
            self.__index = 0
        item = self.__playlist.get_item(self.__index)
        if item is None:
            return False, "Playlist kosong."
        self.__current = item
        self.__status  = self.PLAYING
        item.increment_play()
        return True, f"[{self.__index + 1}/{self.__playlist.total_lagu}] {item}"

    def pause(self):
        if self.__status != self.PLAYING:
            return False, "Tidak sedang memutar lagu."
        self.__status = self.PAUSED
        return True, f"Dijeda: {self.__current}"

    def next(self):
        if self.__playlist is None or self.__playlist.total_lagu == 0:
            return False, "Tidak ada playlist atau playlist kosong."
        self.__index  = (self.__index + 1) % self.__playlist.total_lagu
        self.__status = self.STOPPED
        return self.play()

    def prev(self):
        if self.__playlist is None or self.__playlist.total_lagu == 0:
            return False, "Tidak ada playlist atau playlist kosong."
        self.__index  = (self.__index - 1) % self.__playlist.total_lagu
        self.__status = self.STOPPED
        return self.play()

    def shuffle(self):
        if self.__playlist is None:
            return False, "Tidak ada playlist yang dimuat."
        if self.__playlist.is_shuffled:
            self.__playlist.unshuffle()
            self.__index = 0
            return True, "Shuffle OFF - urutan dikembalikan."
        else:
            ok = self.__playlist.shuffle()
            if not ok:
                return False, "Playlist kosong."
            self.__index = 0
            return True, "Shuffle ON."

    def __str__(self) -> str:
        return f"Player(status={self.__status})"