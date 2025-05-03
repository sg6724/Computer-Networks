import socket

server = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
server.bind(('localhost', 1234))

print("Server started")
data , addr = server.recvfrom(1024)
server.sendto(b"Hello , client! I am server", addr)
msg = data.decode()
print(msg)

server.close()