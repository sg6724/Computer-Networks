import ipaddress

def get_ip_class(ip):
    first_octet = int(ip.split('.')[0])
    if 0 <= first_octet <= 127:
        return 'A'
    elif 128 <= first_octet <= 191:
        return 'B'
    elif 192 <= first_octet <= 223:
        return 'C'
    elif 224 <= first_octet <= 239:
        return 'D (Multicast)'
    elif 240 <= first_octet <= 255:
        return 'E (Reserved)'
    else:
        return 'Invalid'

def analyze_ip(ip_with_mask):
    try:
        network = ipaddress.ip_network(ip_with_mask, strict=False)
    except ValueError as e:
        print(f"Error: {e}")
        return

    ip = str(network.network_address)
    subnet_mask = str(network.netmask)
    broadcast = str(network.broadcast_address)
    ip_class = get_ip_class(ip)
    total_hosts = network.num_addresses

    if total_hosts > 2:
        first_usable = str(list(network.hosts())[0])
        last_usable = str(list(network.hosts())[-1])
    else:
        first_usable = last_usable = "Not available (too small subnet)"

    print(f"\n[+] IP Analysis of {ip_with_mask}")
    print(f"    ➤ IP Class          : {ip_class}")
    print(f"    ➤ Subnet Mask       : {subnet_mask}")
    print(f"    ➤ Network Address   : {ip}")
    print(f"    ➤ Broadcast Address : {broadcast}")
    print(f"    ➤ First Usable IP   : {first_usable}")
    print(f"    ➤ Last Usable IP    : {last_usable}")
    print(f"    ➤ Total IPs in Block: {total_hosts}")

# --- Driver Code ---
if __name__ == "__main__":
    ip_input = input("Enter IP address with subnet (e.g., 192.168.1.10/24): ")
    analyze_ip(ip_input)
