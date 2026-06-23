from music_classes import Lagu, Podcast, Playlist, Player
import threading
import time


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
    while True:
        raw = input("  Durasi (MM:SS): ").strip()
        try:
            return Lagu.parse_durasi(raw)
        except ValueError as e:
            print(f"  Format tidak valid -- {e}.")


def input_lagu() -> Lagu:
    print("\n  [Input Lagu Baru]")
    judul  = input_tidak_kosong("  Judul : ")
    artis  = input_tidak_kosong("  Artis : ")
    genre  = input("  Genre : ").strip() or "Unknown"
    durasi = input_durasi()
    return Lagu(judul, artis, durasi, genre)


def input_podcast() -> Podcast:
    print("\n  [Input Podcast Baru]")
    judul = input_tidak_kosong("  Judul Podcast : ")
    host  = input_tidak_kosong("  Host           : ")
    durasi = input_durasi()
    while True:
        ep_raw = input("  Episode (angka): ").strip()
        if ep_raw.isdigit() and int(ep_raw) > 0:
            episode = int(ep_raw)
            break
        print("  Episode harus angka positif.")
    return Podcast(judul, host, durasi, episode)


def pilih_media_untuk_playlist(pl: Playlist, media_pool: list) -> int:
    print("\n  Pilih item (nomor dipisah koma):")
    for i, m in enumerate(media_pool, 1):
        print(f"  {i}. {m}")

    while True:
        raw = input("  Pilihan: ").strip()
        if not raw:
            print("  Harus memilih minimal 1 item.")
            continue

        # Validasi pemisah: tolak '.' dan karakter non-valid
        token_list = []
        valid = True
        for token in raw.replace(",", " ").split():
            if not token.isdigit():
                print(f"  '{token}' bukan angka yang valid. Gunakan koma sebagai pemisah (contoh: 1,2,3)")
                valid = False
                break
            token_list.append(int(token) - 1)

        if not valid:
            continue

        # Validasi rentang
        invalid = [t + 1 for t in token_list if not (0 <= t < len(media_pool))]
        if invalid:
            print(f"  Nomor tidak valid: {invalid}. Pilih antara 1 dan {len(media_pool)}.")
            continue

        # Semua valid, tambahkan
        ditambahkan = 0
        for idx in token_list:
            pl.tambah_lagu(media_pool[idx])
            print(f"  Ditambahkan: {media_pool[idx]}")
            ditambahkan += 1
        return ditambahkan


def input_playlist(media_pool: list) -> Playlist | None:
    print("\n  [Input Playlist Baru]")

    if not media_pool:
        print("  Belum ada lagu/podcast. Tambahkan item terlebih dahulu sebelum membuat playlist.")
        return None

    nama = input_tidak_kosong("  Nama Playlist: ")
    pl   = Playlist(nama)

    jumlah = pilih_media_untuk_playlist(pl, media_pool)
    if jumlah == 0:
        print("  Playlist tidak dibuat karena tidak ada item yang dipilih.")
        return None

    return pl


# ─────────────────────────────────────────────
#  MENU DATA
# ─────────────────────────────────────────────

def menu_edit_media(media_pool: list):
    if not media_pool:
        print("  Belum ada lagu/podcast.")
        return
    print("\n  Pilih item yang akan diedit:")
    for i, m in enumerate(media_pool, 1):
        print(f"  {i}. {m}")
    try:
        idx = int(input("  Nomor: ").strip()) - 1
        if not (0 <= idx < len(media_pool)):
            print("  Nomor tidak valid.")
            return
    except ValueError:
        print("  Input tidak valid.")
        return

    item = media_pool[idx]
    print(f"\n  Edit item: {item}")
    print("  (Kosongkan untuk mempertahankan nilai lama)")

    if isinstance(item, Lagu):
        judul_baru = input(f"  Judul [{item.judul}]: ").strip()
        artis_baru = input(f"  Artis [{item.artis}]: ").strip()
        genre_baru = input(f"  Genre [{item.genre}]: ").strip()
        if judul_baru:
            item.judul = judul_baru
        if artis_baru:
            item.artis = artis_baru
        if genre_baru:
            item.genre = genre_baru

    elif isinstance(item, Podcast):
        judul_baru = input(f"  Judul [{item.judul}]: ").strip()
        host_baru  = input(f"  Host  [{item.host}]: ").strip()
        if judul_baru:
            item.judul = judul_baru
        if host_baru:
            item.host = host_baru

    print(f"  Durasi saat ini: {item.format_durasi()}")
    durasi_raw = input("  Durasi baru (MM:SS, kosong=skip): ").strip()
    if durasi_raw:
        try:
            item.set_durasi(Lagu.parse_durasi(durasi_raw))
        except ValueError as e:
            print(f"  Durasi tidak diubah -- {e}")

    print(f"  Item berhasil diperbarui: {item}")


def menu_edit_playlist(playlist_pool: list, media_pool: list):
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
        print("  2. Tambah item")
        print("  3. Hapus item")
        print("  0. Selesai")
        pilihan = input("  Pilihan: ").strip()

        if pilihan == "1":
            nama_baru = input_tidak_kosong("  Nama baru: ")
            pl.nama = nama_baru
            print(f"  Nama diubah menjadi: {pl.nama}")

        elif pilihan == "2":
            if not media_pool:
                print("  Belum ada lagu/podcast.")
            else:
                pilih_media_untuk_playlist(pl, media_pool)

        elif pilihan == "3":
            aktif = pl.get_original_list()
            if not aktif:
                print("  Playlist kosong.")
            else:
                print("\n  Pilih item yang dihapus:")
                for i, m in enumerate(aktif, 1):
                    print(f"  {i}. {m}")
                judul = input("  Judul item: ").strip()
                if pl.hapus_lagu(judul):
                    print(f"  '{judul}' dihapus dari playlist.")
                else:
                    print(f"  '{judul}' tidak ditemukan.")

        elif pilihan == "0":
            break
        else:
            print("  Pilihan tidak valid.")


def menu_data(media_pool: list, playlist_pool: list):
    while True:
        print("\n  [MENU DATA]")
        print("  1. Tambah Lagu")
        print("  2. Tambah Podcast")
        print("  3. Tambah Playlist")
        print("  4. Edit Lagu/Podcast")
        print("  5. Edit Playlist")
        print("  6. Lihat Semua Data")
        print("  0. Kembali")
        pilihan = input("  Pilihan: ").strip()

        if pilihan == "1":
            lagu = input_lagu()
            media_pool.append(lagu)
            print(f"  Lagu ditambahkan: {lagu}")

        elif pilihan == "2":
            podcast = input_podcast()
            media_pool.append(podcast)
            print(f"  Podcast ditambahkan: {podcast}")

        elif pilihan == "3":
            pl = input_playlist(media_pool)
            if pl is not None:
                playlist_pool.append(pl)
                print(f"  Playlist dibuat: {pl.nama} ({pl.total_lagu} item)")

        elif pilihan == "4":
            menu_edit_media(media_pool)

        elif pilihan == "5":
            menu_edit_playlist(playlist_pool, media_pool)

        elif pilihan == "6":
            print("\n  === DAFTAR LAGU & PODCAST ===")
            if media_pool:
                for i, m in enumerate(media_pool, 1):
                    print(f"  {i}. {m.get_info()}")
            else:
                print("  (Belum ada lagu/podcast)")
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
#  TAMPILAN PLAYLIST
# ─────────────────────────────────────────────

def _tampilkan_playlist(pl: Playlist, active_list: list = None, current_index: int = -1):
    daftar = active_list if active_list is not None else pl.get_original_list()
    total_detik = sum(item.get_duration() for item in daftar)
    total_fmt   = f"{total_detik // 60:02d}:{total_detik % 60:02d}"

    print(f"\n  {'─'*48}")
    print(f"  Playlist : {pl.nama}")
    print(f"  Total    : {len(daftar)} lagu | Durasi: {total_fmt}")
    print(f"  Shuffle  : {'ON' if pl.is_shuffled else 'OFF'}")
    print(f"  {'─'*48}")
    if not daftar:
        print("  (Playlist kosong)")
    for i, item in enumerate(daftar):
        marker = " << NOW PLAYING" if i == current_index else ""
        print(f"  {i+1:>2}. {item}{marker}")
    print(f"  {'─'*48}")


# ─────────────────────────────────────────────
#  TIMER DISPLAY
# ─────────────────────────────────────────────

_display_lock = threading.Lock()


def _print_timer(player: Player):
    if player.status == Player.PLAYING and player.current:
        sisa = player.format_sisa()
        total = player.current.format_durasi()
        persen = 0
        if player.current.get_duration() > 0:
            persen = max(0, 100 - int(player.sisa_detik / player.current.get_duration() * 100))
        bar_len  = 20
        filled   = int(bar_len * persen / 100)
        bar      = "#" * filled + "-" * (bar_len - filled)
        with _display_lock:
            print(f"\r  [{bar}] {persen:3d}%  sisa: {sisa} / {total}   ", end="", flush=True)


def _timer_display_loop(player: Player, stop_evt: threading.Event):
    while not stop_evt.is_set():
        if player.status == Player.PLAYING:
            _print_timer(player)
        time.sleep(1)
    print("\r" + " " * 60 + "\r", end="", flush=True)


# ─────────────────────────────────────────────
#  MENU PLAYER
# ─────────────────────────────────────────────

def menu_player(player: Player, playlist_pool: list):
    # Thread display timer
    stop_display = threading.Event()
    display_thread = threading.Thread(
        target=_timer_display_loop, args=(player, stop_display), daemon=True
    )
    display_thread.start()

    # Callback auto-next saat lagu habis
    def on_song_end():
        # Jeda sebentar agar timer sempat sampai 00:00
        time.sleep(0.5)
        ok, msg = player.next()
        with _display_lock:
            print(f"\n  [Auto] {msg}")

    player.set_auto_next_callback(on_song_end)

    try:
        while True:
            print(f"\n\n  [MENU PLAYER]  Status: {player.status}"
                  + (" | Shuffle ON" if player.is_shuffled else ""))
            print("  1. Muat Playlist")
            print("  2. Play")
            print("  3. Pause")
            print("  4. Next")
            print("  5. Prev")
            print("  6. Shuffle (acak ulang)")
            print("  7. Unshuffle (urutan asli)")
            print("  8. Now Playing")
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
                ok, pesan = player.unshuffle()
                print(f"  {pesan}")

            elif pilihan == "8":
                pl = player.playlist
                if pl is None:
                    print("  Tidak ada playlist yang dimuat.")
                else:
                    # Tampilkan playlist + posisi lagu aktif
                    idx = player.current_index if player.status != Player.STOPPED else -1
                    _tampilkan_playlist(pl, active_list=player.active_list, current_index=idx)
                    # Info timer
                    if player.status == Player.PLAYING and player.current:
                        print(f"  Lagu    : {player.current}")
                        print(f"  Status  : {player.status}")
                        print(f"  Sisa    : {player.format_sisa()} / {player.current.format_durasi()}")
                    elif player.status == Player.PAUSED and player.current:
                        print(f"  Lagu    : {player.current}")
                        print(f"  Status  : PAUSED -- sisa {player.format_sisa()}")

            elif pilihan == "0":
                break
            else:
                print("  Pilihan tidak valid.")
    finally:
        stop_display.set()
        player.set_auto_next_callback(None)


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────

def main():
    garis()
    print("  APLIKASI MUSIK PLAYER")
    garis()

    media_pool:    list     = []
    playlist_pool: list[Playlist] = []
    player = Player()

    while True:
        garis()
        print("  MENU UTAMA")
        garis()
        print("  1. Data (Lagu, Podcast & Playlist)")
        print("  2. Player")
        print("  0. Keluar")
        pilihan = input("  Pilihan: ").strip()

        if pilihan == "1":
            menu_data(media_pool, playlist_pool)
        elif pilihan == "2":
            menu_player(player, playlist_pool)
        elif pilihan == "0":
            print("\n  Sampai jumpa!\n")
            break
        else:
            print("  Pilihan tidak valid.")


if __name__ == "__main__":
    main()