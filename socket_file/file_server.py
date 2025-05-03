import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 1235))
server.listen(1)

print("Server ready to send file...")
conn, addr = server.accept()
print("Connected with", addr)

filename = "send_file.txt"
with open(filename, 'rb') as f:
    data = f.read()
    conn.sendall(data)
print("File sent.")

conn.close()
