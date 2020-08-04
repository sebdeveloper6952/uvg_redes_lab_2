import socket
from bitarray import bitarray
from hamming import Hamming

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 6969        # Port to listen on (non-privileged ports are > 1023)
PACKET_SIZE = 128

decoder = Hamming()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(PACKET_SIZE)
            if not data:
                print('Received empty, close connection.')
                break
            b = bitarray()
            b.frombytes(data)
            if (len(b) % 12 != 0):
                b = b[:-4]
            decoder.decode(data=b)
            print(f'Decoded: {decoder.hamming_decoded}')
            conn.send(b'1')