"""
=============================================================
  FILE: main.py
  Deskripsi: Program Utama -- Input objek & simulasi Player
  Import dari: music_classes.py
=============================================================
"""

from music_classes import Lagu, Playlist, Player


# ─────────────────────────────────────────────
#  HELPER
# ─────────────────────────────────────────────

def garis():
    print("─" * 50)


def input_tidak_kosong(prompt: str) -> str:
    while True:
        nilai = input(prompt).strip()
        if nilai:
            return nilai
        print("  Input tidak boleh kosong!")


def input_durasi() -> int:
    """Input durasi format MM:SS dengan validasi."""
    while True:
        raw = input("  Durasi (MM:SS): ").strip()
        try:
            return Lagu.parse_durasi(raw)
        except ValueError as e:
            print(f"  Format tidak valid -- {e}. Contoh: 03:45")


def input_lagu() -> Lagu:
    print("\n  [Input Lagu Baru]")
    judul  = input_tidak_kosong("  Judul : ")
    artis  = input_tidak_kosong("  Artis : ")
    genre  = input("  Genre : ").strip() or "Unknown"
    durasi = input_durasi()
    return Lagu(judul, artis, durasi, genre)


def input_playlist(lagu_pool: list) -> Playlist:
    print("\n  [Input Playlist Baru]")
    nama = input_tidak_kosong("  Nama Playlist: ")
    pl   = Playlist(nama)
    if not lagu_pool:
        print("  Belum ada lagu. Playlist dibuat kosong.")
        return pl
    pilih_lagu_untuk_playlist(pl, lagu_pool)
    return pl


def pilih_lagu_untuk_playlist(pl: Playlist, lagu_pool: list):
    """Tampilkan daftar lagu dan tambahkan pilihan ke playlist."""
    print("\n  Pilih lagu (nomor dipisah koma, kosong=lewati):")
    for i, l in enumerate(lagu_pool, 1):
        print(f"  {i}. {l}")
    raw = input("  Pilihan: ").strip()
    if not raw:
        return
    try:
        for x in raw.split(","):
            idx = int(x.strip()) - 1
            if 0 <= idx < len(lagu_pool):
                pl.tambah_lagu(lagu_pool[idx])
                print(f"  Ditambahkan: {lagu_pool[idx]}")
            else:
                print(f"  Nomor {idx+1} tidak valid, dilewati.")
    except ValueError:
        print("  Format tidak valid, tidak ada lagu ditambahkan.")


# ─────────────────────────────────────────────
#  MENU DATA
# ─────────────────────────────────────────────

def menu_edit_lagu(lagu_pool: list):
    if not lagu_pool:
        print("  Belum ada lagu.")
        return
    print("\n  Pilih lagu yang akan diedit:")
    for i, l in enumerate(lagu_pool, 1):
        print(f"  {i}. {l}")
    try:
        idx = int(input("  Nomor: ").strip()) - 1
        if not (0 <= idx < len(lagu_pool)):
            print("  Nomor tidak valid.")
            return
    except ValueError:
        print("  Input tidak valid.")
        return

    lagu = lagu_pool[idx]
    print(f"\n  Edit lagu: {lagu}")
    print("  (Kosongkan untuk mempertahankan nilai lama)")

    judul_baru = input(f"  Judul [{lagu.judul}]: ").strip()
    artis_baru = input(f"  Artis [{lagu.artis}]: ").strip()
    genre_baru = input(f"  Genre [{lagu.genre}]: ").strip()
    print(f"  Durasi saat ini: {lagu.format_durasi()}")
    durasi_raw = input("  Durasi baru (MM:SS, kosong=skip): ").strip()

    if judul_baru:
        lagu.judul = judul_baru
    if artis_baru:
        lagu.artis = artis_baru
    if genre_baru:
        lagu.genre = genre_baru
    if durasi_raw:
        try:
            lagu.set_durasi(Lagu.parse_durasi(durasi_raw))
        except ValueError as e:
            print(f"  Durasi tidak diubah -- {e}")

    print(f"  Lagu berhasil diperbarui: {lagu}")


def menu_edit_playlist(playlist_pool: list, lagu_pool: list):
    if not playlist_pool:
        print("  Belum ada playlist.")
        return
    print("\n  Pilih playlist yang akan diedit:")
    for i, pl in enumerate(playlist_pool, 1):
        print(f"  {i}. {pl}")
    try:
        idx = int(input("  Nomor: ").strip()) - 1
        if not (0 <= idx < len(playlist_pool)):
            print("  Nomor tidak valid.")
            return
    except ValueError:
        print("  Input tidak valid.")
        return

    pl = playlist_pool[idx]
    print(f"\n  Edit playlist: {pl}")

    while True:
        print("\n  [Edit Playlist]")
        print("  1. Ganti nama")
        print("  2. Tambah lagu")
        print("  3. Hapus lagu")
        print("  0. Selesai")
        pilihan = input("  Pilihan: ").strip()

        if pilihan == "1":
            nama_baru = input_tidak_kosong("  Nama baru: ")
            pl.nama = nama_baru
            print(f"  Nama diubah menjadi: {pl.nama}")

        elif pilihan == "2":
            if not lagu_pool:
                print("  Belum ada lagu.")
            else:
                pilih_lagu_untuk_playlist(pl, lagu_pool)

        elif pilihan == "3":
            aktif = pl.get_active_list()
            if not aktif:
                print("  Playlist kosong.")
            else:
                print("\n  Pilih lagu yang dihapus:")
                for i, l in enumerate(aktif, 1):
                    print(f"  {i}. {l}")
                judul = input("  Judul lagu: ").strip()
                if pl.hapus_lagu(judul):
                    print(f"  '{judul}' dihapus dari playlist.")
                else:
                    print(f"  '{judul}' tidak ditemukan.")

        elif pilihan == "0":
            break
        else:
            print("  Pilihan tidak valid.")


def menu_data(lagu_pool: list, playlist_pool: list):
    while True:
        print("\n  [MENU DATA]")
        print("  1. Tambah Lagu")
        print("  2. Tambah Playlist")
        print("  3. Edit Lagu")
        print("  4. Edit Playlist")
        print("  5. Lihat Semua Data")
        print("  0. Kembali")
        pilihan = input("  Pilihan: ").strip()

        if pilihan == "1":
            lagu = input_lagu()
            lagu_pool.append(lagu)
            print(f"  Lagu ditambahkan: {lagu}")

        elif pilihan == "2":
            pl = input_playlist(lagu_pool)
            playlist_pool.append(pl)
            print(f"  Playlist dibuat: {pl.nama}")

        elif pilihan == "3":
            menu_edit_lagu(lagu_pool)

        elif pilihan == "4":
            menu_edit_playlist(playlist_pool, lagu_pool)

        elif pilihan == "5":
            print("\n  === DAFTAR LAGU ===")
            if lagu_pool:
                for i, l in enumerate(lagu_pool, 1):
                    print(f"  {i}. {l.get_info()}")
            else:
                print("  (Belum ada lagu)")
            print("\n  === DAFTAR PLAYLIST ===")
            if playlist_pool:
                for pl in playlist_pool:
                    _tampilkan_playlist(pl)
            else:
                print("  (Belum ada playlist)")

        elif pilihan == "0":
            break
        else:
            print("  Pilihan tidak valid.")


# ─────────────────────────────────────────────
#  HELPER TAMPIL PLAYLIST
# ─────────────────────────────────────────────

def _tampilkan_playlist(pl: Playlist, current_index: int = -1):
    """Tampilkan isi playlist. Tandai lagu aktif jika current_index >= 0."""
    print(f"\n  {'─'*48}")
    print(f"  Playlist : {pl.nama}")
    print(f"  Total    : {pl.total_lagu} lagu | Durasi: {pl.total_durasi}")
    print(f"  Shuffle  : {'ON' if pl.is_shuffled else 'OFF'}")
    print(f"  {'─'*48}")
    aktif = pl.get_active_list()
    if not aktif:
        print("  (Playlist kosong)")
    for i, item in enumerate(aktif):
        marker = " >> PLAYING" if i == current_index else ""
        print(f"  {i+1:>2}. {item}{marker}")
    print(f"  {'─'*48}")


# ─────────────────────────────────────────────
#  MENU PLAYER
# ─────────────────────────────────────────────

def menu_player(player: Player, playlist_pool: list):
    while True:
        print(f"\n  [MENU PLAYER]  Status: {player.status}")
        print("  1. Muat Playlist")
        print("  2. Play")
        print("  3. Pause")
        print("  4. Next")
        print("  5. Prev")
        print("  6. Shuffle")
        print("  7. Lihat Playlist & Posisi")
        print("  0. Kembali")
        pilihan = input("  Pilihan: ").strip()

        if pilihan == "1":
            if not playlist_pool:
                print("  Belum ada playlist.")
            else:
                for i, pl in enumerate(playlist_pool, 1):
                    print(f"  {i}. {pl}")
                try:
                    idx = int(input("  Nomor: ")) - 1
                    if 0 <= idx < len(playlist_pool):
                        player.load(playlist_pool[idx])
                        print(f"  Playlist '{playlist_pool[idx].nama}' dimuat.")
                    else:
                        print("  Nomor tidak valid.")
                except ValueError:
                    print("  Input tidak valid.")

        elif pilihan == "2":
            ok, pesan = player.play()
            print(f"  {pesan}")

        elif pilihan == "3":
            ok, pesan = player.pause()
            print(f"  {pesan}")

        elif pilihan == "4":
            ok, pesan = player.next()
            print(f"  {pesan}")

        elif pilihan == "5":
            ok, pesan = player.prev()
            print(f"  {pesan}")

        elif pilihan == "6":
            ok, pesan = player.shuffle()
            print(f"  {pesan}")

        elif pilihan == "7":
            pl = player.playlist
            if pl is None:
                print("  Tidak ada playlist yang dimuat.")
            else:
                idx = player.current_index if player.status != Player.STOPPED else -1
                _tampilkan_playlist(pl, current_index=idx)

        elif pilihan == "0":
            break
        else:
            print("  Pilihan tidak valid.")


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────

def main():
    garis()
    print("  APLIKASI MUSIK PLAYER")
    garis()

    lagu_pool:     list[Lagu]     = []
    playlist_pool: list[Playlist] = []
    player = Player()

    while True:
        garis()
        print("  MENU UTAMA")
        garis()
        print("  1. Data (Lagu & Playlist)")
        print("  2. Player")
        print("  0. Keluar")
        pilihan = input("  Pilihan: ").strip()

        if pilihan == "1":
            menu_data(lagu_pool, playlist_pool)
        elif pilihan == "2":
            menu_player(player, playlist_pool)
        elif pilihan == "0":
            print("\n  Sampai jumpa!\n")
            break
        else:
            print("  Pilihan tidak valid.")


if __name__ == "__main__":
    main()