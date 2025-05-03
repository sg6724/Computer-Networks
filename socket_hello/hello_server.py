import socket## TCP Transmission

server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
server.bind(('localhost', 123))
server.listen(1)

conn , addr = server.accept()

print("Connected to addres",addr)

conn.sendall(b"Hello from server")
msg = conn.recv(1024).decode()
print(msg)
conn.close()