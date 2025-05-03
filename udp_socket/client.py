import socket

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto(b"Hello, server! I am client",('localhost', 1234))
data , addr = client.recvfrom(1024)
print("Received from server: ", data.decode())
client.close()
