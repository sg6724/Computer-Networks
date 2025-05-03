import socket

def dns_lookup():
    choice = input("Enter 1 for URL → IP lookup\nEnter 2 for IP → URL lookup\nChoice: ")

    if choice == '1':
        domain = input("Enter domain name (e.g., www.google.com): ")
        try:
            ip = socket.gethostbyname(domain)
            print(f"IP address of {domain} is {ip}")
        except socket.gaierror:
            print("Invalid domain name or DNS lookup failed.")
    elif choice == '2':
        ip = input("Enter IP address (e.g., 8.8.8.8): ")
        try:
            host = socket.gethostbyaddr(ip)
            print(f"Domain name for IP {ip} is {host[0]}")
        except socket.herror:
            print("Could not find domain name for the IP.")
    else:
        print("Invalid choice.")

# 🧪 Run the program
if __name__ == "__main__":
    dns_lookup()
