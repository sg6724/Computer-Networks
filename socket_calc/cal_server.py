import socket

def calculate(expr):
    try:
        return str(eval(expr))
    except Exception as e:
        return f"Error: {e}"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 1236))
server.listen(1)
print("Calculator Server is running...")

conn, addr = server.accept()
print("Connected to", addr)

expr = conn.recv(1024).decode()
print("Expression from client:", expr)

result = calculate(expr)
conn.sendall(result.encode())

conn.close()
