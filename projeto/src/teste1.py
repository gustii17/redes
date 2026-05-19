import socket

HOST_IP = "127.0.0.1"
PORT = 61432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM,) as s:
    s.connect((HOST_IP, PORT))
    s.sendall(b"1 a1")
    data = s.recv(1024)

print(f"Recebido do server: {data!r}")
