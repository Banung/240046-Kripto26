import numpy as np
from sympy import Matrix
import re

def char_to_num(c):
    return ord(c) - 65

def num_to_char(n):
    return chr(n + 65)

def get_mod_inverse(matrix, mod=26):
    """Mencari invers matriks modulo 26."""
    try:
        # Sympy memiliki fungsi bawaan inv_mod untuk mencari invers matriks modular
        inv_matrix = Matrix(matrix).inv_mod(mod)
        return np.array(inv_matrix).astype(int)
    except ValueError:
        return None

def encrypt_hill(plaintext, key_matrix):
    """Fungsi untuk enkripsi teks menggunakan Hill Cipher."""
    # Bersihkan teks: ubah ke uppercase dan hilangkan karakter non-alfabet
    plaintext = re.sub(r'[^A-Z]', '', plaintext.upper())
    
    m = len(key_matrix)
    # Tambahkan padding 'X' jika panjang teks tidak kelipatan ukuran matriks kunci
    while len(plaintext) % m != 0:
        plaintext += 'X'
        
    key_matrix = np.array(key_matrix)
    ciphertext = ""
    
    for i in range(0, len(plaintext), m):
        block = [char_to_num(c) for c in plaintext[i:i+m]]
        # Perkalian matriks: C = K * P mod 26
        result = np.dot(key_matrix, block) % 26
        ciphertext += "".join([num_to_char(c) for c in result])
        
    return ciphertext

def decrypt_hill(ciphertext, key_matrix):
    """Fungsi untuk dekripsi teks menggunakan Hill Cipher."""
    ciphertext = re.sub(r'[^A-Z]', '', ciphertext.upper())
    m = len(key_matrix)
    
    inv_key = get_mod_inverse(key_matrix, 26)
    if inv_key is None:
        raise ValueError("Kunci tidak memiliki invers modulo 26, teks tidak bisa didekripsi.")
        
    plaintext = ""
    for i in range(0, len(ciphertext), m):
        block = [char_to_num(c) for c in ciphertext[i:i+m]]
        # Perkalian matriks: P = K^-1 * C mod 26
        result = np.dot(inv_key, block) % 26
        plaintext += "".join([num_to_char(c) for c in result])
        
    return plaintext

def find_key_hill(plaintext, ciphertext, m):
    """
    Mencari kunci (matriks K) jika Plaintext dan Ciphertext diketahui.
    Rumus: C = K * P mod 26  -->  K = C * P^-1 mod 26
    """
    pt = re.sub(r'[^A-Z]', '', plaintext.upper())
    ct = re.sub(r'[^A-Z]', '', ciphertext.upper())
    
    if len(pt) < m*m or len(ct) < m*m:
        raise ValueError(f"Teks terlalu pendek. Butuh minimal {m*m} karakter untuk kunci {m}x{m}.")
    
    # Ambil m*m karakter pertama untuk membuat matriks P dan C
    P_matrix = []
    C_matrix = []
    
    for i in range(m):
        P_row = [char_to_num(c) for c in pt[i*m : (i+1)*m]]
        C_row = [char_to_num(c) for c in ct[i*m : (i+1)*m]]
        P_matrix.append(P_row)
        C_matrix.append(C_row)
        
    # Transpose karena blok karakter bertindak sebagai vektor kolom
    P = np.array(P_matrix).T
    C = np.array(C_matrix).T
    
    P_inv = get_mod_inverse(P, 26)
    if P_inv is None:
        raise ValueError("Kombinasi plaintext ini matriksnya tidak invertible mod 26. Coba gunakan bagian teks yang lain.")
        
    # K = C * P^-1 mod 26
    K = np.dot(C, P_inv) % 26
    return K.astype(int).tolist()

# ==========================================
# PROGRAM UTAMA (MENU INTERAKTIF)
# ==========================================
def input_matriks_kunci():
    """Meminta ukuran matriks dan isi matriks kunci dari input pengguna."""
    while True:
        try:
            n = int(input("Masukkan ukuran matriks kunci (n untuk n x n): ").strip())
            if n <= 0:
                print("Ukuran matriks harus lebih dari 0.")
                continue
            break
        except ValueError:
            print("Masukkan angka bulat yang valid.")

    matrix = []
    print(f"Masukkan {n} baris, tiap baris berisi {n} angka dipisahkan spasi.")
    for i in range(n):
        while True:
            baris_input = input(f"Baris ke-{i + 1}: ").strip()
            try:
                baris = [int(x) for x in baris_input.split()]
                if len(baris) != n:
                    print(f"Jumlah angka harus {n}, coba lagi.")
                    continue
                matrix.append(baris)
                break
            except ValueError:
                print("Masukkan hanya angka bulat yang dipisahkan spasi.")

    return matrix


def tampilkan_menu():
    print("\n=== HILL CIPHER ===")
    print("1. Enkripsi")
    print("2. Dekripsi")
    print("3. Cari Kunci (dari Plaintext & Ciphertext)")
    print("4. Keluar")


def main():
    while True:
        tampilkan_menu()
        pilihan = input("Pilih menu (1/2/3/4): ").strip()

        if pilihan == "1":
            plaintext = input("Masukkan plaintext : ")
            key = input_matriks_kunci()
            try:
                ciphertext = encrypt_hill(plaintext, key)
                print(f"\nHasil Enkripsi (Ciphertext) : {ciphertext}")
            except Exception as e:
                print(f"\nGagal enkripsi: {e}")

        elif pilihan == "2":
            ciphertext = input("Masukkan ciphertext : ")
            key = input_matriks_kunci()
            try:
                plaintext = decrypt_hill(ciphertext, key)
                print(f"\nHasil Dekripsi (Plaintext)  : {plaintext}")
            except Exception as e:
                print(f"\nGagal dekripsi: {e}")

        elif pilihan == "3":
            plaintext = input("Masukkan plaintext  : ")
            ciphertext = input("Masukkan ciphertext : ")
            try:
                m = int(input("Masukkan ukuran matriks kunci (n untuk n x n): ").strip())
                kunci_ditemukan = find_key_hill(plaintext, ciphertext, m=m)
                print(f"\nKunci yang ditemukan:")
                print(np.array(kunci_ditemukan))
            except ValueError as e:
                print(f"\nGagal mencari kunci: {e}")

        elif pilihan == "4":
            print("Keluar dari program. Sampai jumpa!")
            break

        else:
            print("Pilihan tidak valid, silakan coba lagi.")


if __name__ == "__main__":
    main()