import pyzipper
import argparse

# Parsing argumen dari command line
parser = argparse.ArgumentParser(description="\nPenggunaan: python script.py -z <filezip> -p <filepassword.txt>")
parser.add_argument("-z", dest="filezip", help="File arsip zip", required=True)
parser.add_argument("-p", dest="filepassword", help="File kata sandi", required=True)
parsed_args = parser.parse_args()

# Mendapatkan path file zip dan file password dari argumen
filezip_path = parsed_args.filezip
filepassword_path = parsed_args.filepassword

try:
    # Membuka file zip dengan pyzipper
    with pyzipper.AESZipFile(filezip_path) as filezip:
        filepassword = filepassword_path
        found = False

        # Membaca file password dan mencoba setiap kata sandi
        with open(filepassword, 'r') as f:
            for line in f:
                password = line.strip().encode('utf-8')

                try:
                    # Coba ekstrak semua file untuk menguji password
                    filezip.extractall(pwd=password)
                    print(f"\nPassword Ditemukan: {password.decode()}")
                    found = True
                    break
                except RuntimeError as e:
                    # Menangani kesalahan runtime selain password salah
                    if 'Bad password for file' not in str(e):
                        print(f"Terjadi kesalahan: {e}")
                        break
                except pyzipper.BadZipFile:
                    print("Kesalahan: File Zip Rusak")
                    break
                except pyzipper.LargeZipFile:
                    print("Kesalahan: File Zip Terlalu Besar")
                    break
                except pyzipper.ZipDecryptionError:
                    # Ini terjadi jika kata sandi salah
                    pass

        # Jika password tidak ditemukan dalam daftar
        if not found:
            print("\nPassword tidak ditemukan, coba gunakan daftar password yang lebih besar")

except FileNotFoundError as e:
    print(f"Kesalahan: {e}")
