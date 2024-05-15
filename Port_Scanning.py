import nmap
import sys
import time
import threading

def scan_host(ip, ports):
    """
    Melakukan pemindaian pada host dan port tertentu menggunakan Nmap.
    :param ip: IP address dari target yang akan dipindai.
    :param ports: Daftar port yang akan dipindai.
    :return: Hasil scan dalam bentuk dictionary.
    """
    try:
        scanner = nmap.PortScanner()
        return scanner.scan(ip, ports, arguments="-O")
    except nmap.PortScannerError as e:
        print(f"Scan error pada IP {ip}: {e}")
        return None

def save_results(ip, results):
    """
    Menyimpan hasil pemindaian ke dalam file teks.
    :param ip: IP address dari target.
    :param results: Hasil pemindaian yang diperoleh dari Nmap.
    """
    if results:
        host_is_up = "The host is: " + results["scan"][ip]["status"]["state"] + ".\n"
        port_info = ""
        for port in results["scan"][ip]['tcp'].keys():
            port_info += f"The port {port} is: " + results["scan"][ip]['tcp'][port]['state'] + ".\n"
        method_scan = "The method of scanning is: " + results['scan'][ip]['tcp'][80]['reason'] + ".\n"
        guessed_os = "There is a %s percent chance that the host is running %s" % (results['scan'][ip]['osmatch'][0]['accuracy'], results['scan'][ip]['osmatch'][0]['name']) + ".\n"

        with open(f"{ip}.txt", "w") as f:
            f.write(host_is_up + port_info + method_scan + guessed_os)
            f.write("\nReport generated " + time.strftime("%Y-%m-%d_%H:%M:%S GMT", time.gmtime()))
        print(f"Hasil telah disimpan untuk IP {ip}")

def main():
    """
    Fungsi utama untuk menjalankan pemindaian.
    """
    if len(sys.argv) < 3:
        print("Penggunaan: python script.py <IP> <ports>")
        print("Contoh: python script.py 192.168.1.1 80,443")
        sys.exit(1)

    ip = sys.argv[1]
    ports = sys.argv[2]

    print("\nBerjalan.....\n")
    result = scan_host(ip, ports)
    if result:
        save_results(ip, result)
    else:
        print("Pemindaian gagal, periksa log untuk detailnya.")

    print("\nSelesai.....\n")

if __name__ == "__main__":
    main()
