from fletcher import *

import socket
'''
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 6969        # Port to listen on (non-privileged ports are > 1023)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
'''

message = "Hola"

m1 = encode(message)

print("prueba", m1)
print("prueba", add_noise(m1, 5))


m2 = decode(m1)

print(m2)