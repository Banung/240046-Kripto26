import re


def char_to_num(c):
    return ord(c) - 65


def num_to_char(n):
    return chr((n % 26) + 65)


def generate_key_stream(text_len, key):
    """
    Menghasilkan aliran kunci (key stream) sepanjang teks dengan mengulang
    kunci secara terus-menerus hingga sesuai dengan panjang teks.
    """
    key = re.sub(r'[^A-Z]', '', key.upper())
    if len(key) == 0:
        raise ValueError("Kunci tidak boleh kosong / harus mengandung huruf A-Z.")

    key_stream = ""
    for i in range(text_len):
        key_stream += key[i % len(key)]
    return key_stream


def encrypt_vigenere(plaintext, key):
    """
    Fungsi untuk enkripsi teks menggunakan Vigenere Cipher.
    Rumus: Ci = (Pi + Ki) mod 26
    """
    plaintext = re.sub(r'[^A-Z]', '', plaintext.upper())
    key_stream = generate_key_stream(len(plaintext), key)

    ciphertext = ""
    for p_char, k_char in zip(plaintext, key_stream):
        p_num = char_to_num(p_char)
        k_num = char_to_num(k_char)
        c_num = (p_num + k_num) % 26
        ciphertext += num_to_char(c_num)

    return ciphertext


def decrypt_vigenere(ciphertext, key):
    """
    Fungsi untuk dekripsi teks menggunakan Vigenere Cipher.
    Rumus: Pi = (Ci - Ki) mod 26
    """
    ciphertext = re.sub(r'[^A-Z]', '', ciphertext.upper())
    key_stream = generate_key_stream(len(ciphertext), key)

    plaintext = ""
    for c_char, k_char in zip(ciphertext, key_stream):
        c_num = char_to_num(c_char)
        k_num = char_to_num(k_char)
        p_num = (c_num - k_num) % 26
        plaintext += num_to_char(p_num)

    return plaintext


def find_key_vigenere(plaintext, ciphertext):
    """
    Mencari kunci (berulang) jika Plaintext dan Ciphertext (panjang sama) diketahui.
    Rumus: Ki = (Ci - Pi) mod 26
    Hasil yang dikembalikan adalah kunci sepanjang teks (belum tentu periode terkecilnya).
    """
    pt = re.sub(r'[^A-Z]', '', plaintext.upper())
    ct = re.sub(r'[^A-Z]', '', ciphertext.upper())

    if len(pt) != len(ct):
        raise ValueError("Panjang plaintext dan ciphertext harus sama untuk mencari kunci.")

    key = ""
    for p_char, c_char in zip(pt, ct):
        p_num = char_to_num(p_char)
        c_num = char_to_num(c_char)
        k_num = (c_num - p_num) % 26
        key += num_to_char(k_num)

    return key


# ==========================================
# PROGRAM UTAMA (MENU INTERAKTIF)
# ==========================================
def tampilkan_menu():
    print("\n=== VIGENERE CIPHER ===")
    print("1. Enkripsi")
    print("2. Dekripsi")
    print("3. Cari Kunci (dari Plaintext & Ciphertext)")
    print("4. Keluar")


def main():
    while True:
        tampilkan_menu()
        pilihan = input("Pilih menu (1/2/3/4): ").strip()

        if pilihan == "1":
            plaintext = input("Masukkan plaintext  : ")
            kunci = input("Masukkan kunci      : ")
            try:
                ciphertext = encrypt_vigenere(plaintext, kunci)
                print(f"\nHasil Enkripsi (Ciphertext) : {ciphertext}")
            except ValueError as e:
                print(f"\nGagal enkripsi: {e}")

        elif pilihan == "2":
            ciphertext = input("Masukkan ciphertext  : ")
            kunci = input("Masukkan kunci      : ")
            try:
                plaintext = decrypt_vigenere(ciphertext, kunci)
                print(f"\nHasil Dekripsi (Plaintext)  : {plaintext}")
            except ValueError as e:
                print(f"\nGagal dekripsi: {e}")

        elif pilihan == "3":
            plaintext = input("Masukkan plaintext  : ")
            ciphertext = input("Masukkan ciphertext : ")
            try:
                kunci_ditemukan = find_key_vigenere(plaintext, ciphertext)
                print(f"\nKunci (key stream) yang ditemukan : {kunci_ditemukan}")
            except ValueError as e:
                print(f"\nGagal mencari kunci: {e}")

        elif pilihan == "4":
            print("Keluar dari program. Sampai jumpa!")
            break

        else:
            print("Pilihan tidak valid, silakan coba lagi.")


if __name__ == "__main__":
    main()
