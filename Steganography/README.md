# 🔐 LSB Steganography

Program ini mengimplementasikan **steganografi LSB (Least Significant Bit)** menggunakan bahasa pemrograman Python. Steganografi menyembunyikan *keberadaan* pesan, bukan hanya isinya — pesan disisipkan ke bit paling tidak berarti (LSB) pada pixel gambar sehingga perubahan tidak terlihat oleh mata.

Program dapat menyembunyikan **pesan teks** maupun **file apa pun** (misalnya gambar lain) ke dalam sebuah gambar PNG, lalu mengekstraknya kembali.

## ✨ Fitur

1. **Encode** — menyisipkan pesan teks atau file ke dalam *cover image* (PNG) menghasilkan *stego-image*.
2. **Decode** — mengekstrak pesan/file kembali dari *stego-image*.
3. **Dua jenis payload** — teks (UTF-8) atau file biner/gambar apa pun.
4. **Header otomatis** — magic `STG1` + panjang data (4 byte) disisipkan di awal sehingga proses decode tahu berapa banyak data yang harus diambil.
5. **Menu interaktif** — semua input dimasukkan langsung oleh pengguna lewat terminal.
6. **LSB sequential** pada kanal warna R, G, B (kanal alpha tidak dipakai).

## 🛠️ Persyaratan (Requirements)

* Python 3.6+
* `Pillow` (untuk membuka dan menyimpan gambar)

```bash
pip install pillow --break-system-packages
```

## 🚀 Cara Penggunaan

1. Arahkan terminal ke direktori `src`.
2. Jalankan:

```bash
python3 lsb.py
```

3. Menu yang muncul:

```text
=== LSB STEGANOGRAPHY ===
1. Encode (sisipkan pesan ke gambar)
2. Decode (ambil pesan dari stego image)
3. Keluar
Pilih menu (1/2/3):
```

4. **Encode (1)** — masukkan path *cover image* (PNG), path *stego output*, lalu pilih jenis payload (`1` teks atau `2` file). Untuk file, masukkan path file payload.
5. **Decode (2)** — masukkan path *stego-image*. Kosongkan input "Simpan ke file" untuk menampilkan teks, atau isi nama file untuk menyimpan hasil ekstraksi (wajib untuk payload biner/gambar).
6. **Keluar (3)** — menutup program.

## 💻 Contoh Output Program

![contoh.png](conntoh.png)

## 📐 Cara Kerja Program

### 1. Konsep LSB

Setiap pixel citra *true color* (24-bit) tersusun dari 3 komponen warna — Merah (R), Hijau (G), Biru (B) — masing-masing 8 bit. Bit paling kanan (LSB) hanya bernilai 1, sehingga mengubahnya mengubah nilai warna sebesar **maksimal 1** dari 255. Perubahan sekecil ini tidak dapat dibedakan oleh mata manusia.

```text
10010101  (149)
10010100  (148)   <-- hanya LSB yang berubah
```

### 2. Penyisipan (Encode)

Data yang akan disembunyikan diubah menjadi deretan bit, lalu tiap bit menggantikan LSB kanal R, G, B secara berurutan.

```text
Aturan: LSB_kanal = bit_pesan
```

Contoh satu pixel `RGB(130, 123, 117)` = `10000010 01111011 01110101`, pesan bit `101`:

```text
sebelum : 1000001|0  0111101|1  0111010|1
sesudah : 1000001|1  0111101|0  0111010|1
          = RGB(131, 122, 117)
```

### 3. Format Payload

Sebelum data asli, disisipkan header agar decode dapat menentukan batas data:

```text
[ "STG1" (4 byte) ][ panjang data (4 byte, big-endian) ][ data asli ]
```

Total 8 byte header (64 bit) + data. Kedua bagian header dan data disisipkan dengan cara LSB yang sama.

### 4. Ekstraksi (Decode)

Program membaca LSB kanal R, G, B secara berurutan untuk menyusun kembali byte-byte:

1. Ambil 4 byte pertama → cek magic `STG1` (validasi bahwa gambar memang stego hasil program ini).
2. Ambil 4 byte berikutnya → panjang data `n`.
3. Ambil `n` byte berikutnya → data asli.

### 5. Kapasitas

Karena 1 bit per kanal dan 3 kanal per pixel tanpa alpha:

```text
kapasitas (bit) = lebar × tinggi × 3
kapasitas (byte) = (lebar × tinggi × 3) / 8  − 8 byte header
```

Cover contoh 640 × 400 px menyediakan `640 × 400 × 3 / 8 = 96.000` byte.

## ⚠️ Catatan / Limitasi

* Output **harus PNG** (lossless). Format lossy seperti JPEG akan merusak bit LSB sehingga pesan tidak dapat diekstrak.
* Penyisipan bersifat **sequential** (berurutan dari pixel pertama), bukan acak. Untuk meningkatkan ketahanan terhadap *steganalysis*, dapat dikembangkan mode acak berbasis *stego-key* (PRNG seed) atau *m-bit* LSB.
* Belum ada enkripsi pada payload; keamanan murni bergantung pada penyembunyian (sesuai definisi steganografi).
