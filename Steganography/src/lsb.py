from PIL import Image

MAGIC = b"STG1"
HEADER = 8  # 4 byte magic + 4 byte panjang (big-endian)


def _to_bits(data):
    bits = []
    for byte in data:
        for shift in range(7, -1, -1):
            bits.append((byte >> shift) & 1)
    return bits


def _lsb_bits(img):
    """Generator bit LSB berurutan dari kanal R,G,B tiap pixel."""
    px = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            for c in px[x, y][:3]:
                yield c & 1


def _take_bytes(bits_gen, n):
    out = bytearray()
    for _ in range(n):
        byte = 0
        for _ in range(8):
            byte = (byte << 1) | next(bits_gen)
        out.append(byte)
    return bytes(out)


def embed(cover_path, data):
    """Sisipkan `data` (bytes) ke cover image, kembalikan PIL.Image stego."""
    payload = MAGIC + len(data).to_bytes(4, "big") + data
    bits = _to_bits(payload)

    img = Image.open(cover_path).convert("RGB")
    w, h = img.size
    if len(bits) > w * h * 3:
        raise ValueError(
            f"Kapasitas kurang: butuh {len(bits)} bit, tersedia {w * h * 3} bit."
        )

    px = img.load()
    idx = 0
    for y in range(h):
        if idx >= len(bits):
            break
        for x in range(w):
            r, g, b = px[x, y]
            new = []
            for c in (r, g, b):
                if idx < len(bits):
                    c = (c & 0xFE) | bits[idx]
                    idx += 1
                new.append(c)
            px[x, y] = tuple(new)
            if idx >= len(bits):
                break
    return img


def extract(stego_path):
    """Ambil kembali data (bytes) dari stego image."""
    img = Image.open(stego_path).convert("RGB")
    gen = _lsb_bits(img)

    if _take_bytes(gen, 4) != MAGIC:
        raise ValueError("Magic bytes tidak cocok. Gambar bukan stego hasil program ini.")

    length = int.from_bytes(_take_bytes(gen, 4), "big")
    return _take_bytes(gen, length)


# ==========================================
# PROGRAM UTAMA (MENU INTERAKTIF)
# ==========================================
def tampilkan_menu():
    print("\n=== LSB STEGANOGRAPHY ===")
    print("1. Encode (sisipkan pesan ke gambar)")
    print("2. Decode (ambil pesan dari stego image)")
    print("3. Keluar")


def main():
    while True:
        tampilkan_menu()
        pilihan = input("Pilih menu (1/2/3): ").strip()

        if pilihan == "1":
            cover = input("Path cover image (PNG) : ").strip()
            output = input("Path stego output (PNG): ").strip()
            print("Jenis payload:\n  1. Teks\n  2. File")
            jenis = input("Pilih (1/2): ").strip()
            try:
                if jenis == "1":
                    data = input("Masukkan pesan teks: ").encode("utf-8")
                elif jenis == "2":
                    path = input("Path file payload: ").strip()
                    with open(path, "rb") as f:
                        data = f.read()
                else:
                    print("Jenis tidak valid.")
                    continue
                embed(cover, data).save(output)
                print(f"\nBerhasil. {len(data)} byte disisipkan ke {output}")
            except (FileNotFoundError, ValueError, OSError) as e:
                print(f"\nGagal encode: {e}")

        elif pilihan == "2":
            stego = input("Path stego image (PNG): ").strip()
            try:
                data = extract(stego)
            except (FileNotFoundError, ValueError, OSError, StopIteration) as e:
                print(f"\nGagal decode: {e}")
                continue
            tujuan = input("Simpan ke file (kosongkan utk tampilkan teks): ").strip()
            if tujuan:
                with open(tujuan, "wb") as f:
                    f.write(data)
                print(f"\nBerhasil. {len(data)} byte disimpan ke {tujuan}")
            else:
                try:
                    print(f"\nPesan ({len(data)} byte): {data.decode('utf-8')}")
                except UnicodeDecodeError:
                    print("\nData biner, tampilkan gagal. Simpan ke file.")

        elif pilihan == "3":
            print("Keluar dari program. Sampai jumpa!")
            break

        else:
            print("Pilihan tidak valid, silakan coba lagi.")


if __name__ == "__main__":
    main()
