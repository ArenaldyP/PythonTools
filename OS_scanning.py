import nmap

def os_fingerprint(target_ip):
    """
    Melakukan OS Scanning
    """
    # Membuat Nmap PortScanner
    scanner = nmap.PortScanner()

    # Deteksi OS
    scanner.scan(target_ip, arguments='-O')

    # Pengecekan OS
    if 'osclass' in scanner[target_ip]['osmatch'][0]:
        os_match = scanner[target_ip]['osmatch'][0]['osclass'][0]
        os_name = os_match['osfamily']
        os_vendor = os_match['vendor']
        os_type = os_match['type']
        os_accuracy = os_match['accuracy']

        print(f"Target IP: {target_ip}")
        print(f"Operating System: {os_name}")
        print(f"Vendor: {os_vendor}")
        print(f"Tipe: {os_type}")
        print(f"Akurasi: {os_accuracy}%")
    else:
        print(f"OS deteksi gagal pada IP {target_ip}")

# Example usage
IP = input("Masukan IP: ")
os_fingerprint(IP)
