from abc import ABC, abstractmethod
import random
import threading
import time


# ============================================================
# ABSTRACTION 
# ============================================================

class Media(ABC):

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
# CLASS: Lagu 
# ============================================================

class Lagu(Media):

    @staticmethod
    def parse_durasi(durasi_str: str) -> int:
        bagian = durasi_str.strip().split(":")
        if len(bagian) != 2:
            raise ValueError("Format harus MM:SS (contoh: 03:45)")
        menit_str, detik_str = bagian
        if not menit_str.isdigit() or not detik_str.isdigit():
            raise ValueError("Menit dan detik harus berupa angka")
        menit = int(menit_str)
        detik = int(detik_str)
        if not (0 <= detik <= 59):
            raise ValueError("Detik harus antara 00 dan 59")
        if menit < 0:
            raise ValueError("Menit tidak boleh negatif")
        if menit == 0 and detik == 0:
            raise ValueError("Durasi tidak boleh 00:00")
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

    # -- Setter --
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
# CLASS: Podcast
# ============================================================

class Podcast(Media):

    def __init__(self, judul: str, host: str, durasi: int, episode: int = 1):
        self.__judul      = judul
        self.__host       = host
        self.__durasi     = durasi
        self.__episode    = episode
        self.__play_count = 0

    # -- Getter --
    @property
    def judul(self) -> str:
        return self.__judul

    @property
    def host(self) -> str:
        return self.__host

    @property
    def episode(self) -> int:
        return self.__episode

    @property
    def play_count(self) -> int:
        return self.__play_count

    # -- Setter --
    @judul.setter
    def judul(self, value: str):
        if not value.strip():
            raise ValueError("Judul tidak boleh kosong.")
        self.__judul = value.strip()

    @host.setter
    def host(self, value: str):
        if not value.strip():
            raise ValueError("Nama host tidak boleh kosong.")
        self.__host = value.strip()

    def set_durasi(self, durasi: int):
        if durasi <= 0:
            raise ValueError("Durasi harus lebih dari 0.")
        self.__durasi = durasi

    # -- Method --
    def increment_play(self):
        self.__play_count += 1

    def format_durasi(self) -> str:
        return f"{self.__durasi // 60:02d}:{self.__durasi % 60:02d}"

    def get_duration(self) -> int:
        return self.__durasi

    # -- Implementasi abstract method (berbeda dari Lagu -- POLYMORPHISM) --
    def get_info(self) -> str:
        return (f"[Podcast] {self.__judul} | Host: {self.__host}"
                f" | Episode: {self.__episode} | Durasi: {self.format_durasi()}"
                f" | Diputar: {self.__play_count}x")

    def __str__(self) -> str:
        return f"[Podcast Ep.{self.__episode}] {self.__judul} - {self.__host} ({self.format_durasi()})"


# ============================================================
# CLASS: Playlist
# ============================================================

class Playlist:

    def __init__(self, nama: str):
        self.__nama        = nama
        self.__lagu_list: list[Media] = []
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
                return True
        return False

    def shuffle(self) -> list:
        if not self.__lagu_list:
            return []
        acak = self.__lagu_list.copy()
        random.shuffle(acak)
        self.__is_shuffled = True
        return acak

    def unshuffle(self):
        self.__is_shuffled = False

    def get_original_list(self) -> list[Media]:
        return list(self.__lagu_list)

    def get_item(self, index: int, dari_list: list = None) -> Media:
        target = dari_list if dari_list is not None else self.__lagu_list
        return target[index] if 0 <= index < len(target) else None

    def __str__(self) -> str:
        return f"Playlist '{self.__nama}' ({self.total_lagu} lagu)"


# ============================================================
# CLASS: Player 
# ============================================================

class Player:

    PLAYING = "PLAYING"
    PAUSED  = "PAUSED"
    STOPPED = "STOPPED"

    def __init__(self):
        self.__status         = self.STOPPED
        self.__playlist       = None
        self.__active_list: list[Media] = []   # urutan aktif (asli/shuffle)
        self.__index          = -1
        self.__current        = None
        self.__is_shuffled    = False

        # Timer
        self.__sisa_detik     = 0       # sisa waktu lagu aktif
        self.__timer_thread   = None
        self.__timer_stop_evt = threading.Event()
        self.__auto_next_cb   = None    # callback dipanggil saat lagu habis

    # -- Getter --
    @property
    def status(self) -> str:
        return self.__status

    @property
    def current(self) -> Media:
        return self.__current

    @property
    def current_index(self) -> int:
        return self.__index

    @property
    def playlist(self) -> Playlist:
        return self.__playlist

    @property
    def is_shuffled(self) -> bool:
        return self.__is_shuffled

    @property
    def sisa_detik(self) -> int:
        return self.__sisa_detik

    @property
    def active_list(self) -> list:
        return list(self.__active_list)

    # -- Timer internal --
    def __start_timer(self):
        """Mulai thread hitung mundur."""
        self.__stop_timer()
        self.__timer_stop_evt.clear()
        self.__timer_thread = threading.Thread(
            target=self.__run_timer, daemon=True
        )
        self.__timer_thread.start()

    def __stop_timer(self):
        """Hentikan thread hitung mundur."""
        if self.__timer_thread and self.__timer_thread.is_alive():
            self.__timer_stop_evt.set()
            self.__timer_thread.join(timeout=2)

    def __run_timer(self):
        """Thread: kurangi sisa_detik setiap 1 detik."""
        while self.__sisa_detik > 0 and not self.__timer_stop_evt.is_set():
            time.sleep(1)
            if self.__timer_stop_evt.is_set():
                break
            self.__sisa_detik = max(0, self.__sisa_detik - 1)
        # Lagu selesai secara alami -- jalankan callback di thread baru
        # agar tidak deadlock saat callback memanggil next() -> stop_timer() -> join()
        if not self.__timer_stop_evt.is_set() and self.__sisa_detik == 0:
            if self.__auto_next_cb:
                threading.Thread(target=self.__auto_next_cb, daemon=True).start()

    def set_auto_next_callback(self, cb):
        self.__auto_next_cb = cb

    # -- Method utama --
    def load(self, playlist: Playlist):
        self.__stop_timer()
        self.__playlist    = playlist
        self.__active_list = playlist.get_original_list()
        self.__index       = -1
        self.__status      = self.STOPPED
        self.__current     = None
        self.__sisa_detik  = 0
        self.__is_shuffled = False

    def play(self):
        if self.__playlist is None:
            return False, "Tidak ada playlist yang dimuat."

        # Resume dari PAUSED
        if self.__status == self.PAUSED and self.__current:
            self.__status = self.PLAYING
            self.__start_timer()
            return True, f"Lanjut: {self.__current}"

        # Mulai dari awal jika belum dimulai
        if self.__index < 0:
            self.__index = 0

        item = self.__playlist.get_item(self.__index, self.__active_list)
        if item is None:
            return False, "Playlist kosong."

        self.__stop_timer()
        self.__current    = item
        self.__status     = self.PLAYING
        self.__sisa_detik = item.get_duration()
        item.increment_play()
        self.__start_timer()

        total = len(self.__active_list)
        pesan = (f"[{self.__index + 1}/{total}] {item}\n"
                 f"     {item.get_info()}")
        return True, pesan

    def pause(self):
        if self.__status != self.PLAYING:
            return False, "Tidak sedang memutar lagu."
        self.__stop_timer()
        self.__status = self.PAUSED
        return True, f"Dijeda: {self.__current}"

    def next(self):
        if not self.__active_list:
            return False, "Playlist kosong."
        self.__stop_timer()
        self.__index  = (self.__index + 1) % len(self.__active_list)
        self.__status = self.STOPPED
        return self.play()

    def prev(self):
        if not self.__active_list:
            return False, "Playlist kosong."
        self.__stop_timer()
        self.__index  = (self.__index - 1) % len(self.__active_list)
        self.__status = self.STOPPED
        return self.play()

    def shuffle(self):
        if self.__playlist is None:
            return False, "Tidak ada playlist yang dimuat."
        if self.__playlist.total_lagu == 0:
            return False, "Playlist kosong."

        acak = self.__playlist.shuffle()
        self.__active_list = acak
        self.__is_shuffled = True
        self.__index       = 0
        self.__stop_timer()
        self.__status  = self.STOPPED
        ok, msg = self.play()
        return ok, "Shuffle: urutan diacak ulang. " + msg

    def unshuffle(self):
        if self.__playlist is None:
            return False, "Tidak ada playlist yang dimuat."
        self.__playlist.unshuffle()
        self.__active_list = self.__playlist.get_original_list()
        self.__is_shuffled = False
        self.__index       = 0
        self.__stop_timer()
        self.__status  = self.STOPPED
        ok, msg = self.play()
        return ok, "Shuffle OFF - urutan dikembalikan. " + msg

    def format_sisa(self) -> str:
        d = self.__sisa_detik
        return f"{d // 60:02d}:{d % 60:02d}"

    def __str__(self) -> str:
        return f"Player(status={self.__status})"