import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 1236))

expr = input("Enter arithmetic expression (e.g., 5 + 3): ")
client.sendall(expr.encode())

result = client.recv(1024).decode()
print("Result from server:", result)

client.close()
