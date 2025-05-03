import socket

client = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
client.connect(('localhost', 123))

msg = client.recv(1024).decode()
client.sendall(b"hello from client")
print(msg)
client.close()