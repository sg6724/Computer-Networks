import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 1235))

data = client.recv(1024*1024)
with open("received_file.txt", 'wb') as f:
    f.write(data)

print("File received successfully!")
client.close()
