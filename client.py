from random import seed, randrange
import socket
from hamming import Hamming
from functools import reduce
from fletcher import *

# hostname servidor/receptor
HOST = '127.0.0.1'
# puerto de servidor/receptor
PORT = 6969
# para reproducibilidad
RANDOM_SEED = 5000
seed(RANDOM_SEED)

ASCII = 'ascii'
UTF = 'latin-1'

HAMMING = 1
FLETCHER = 2
encoder = Hamming()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print('Connected to server!')
    for length in range(1, 50, 5):
        msg = [chr(randrange(97, 123)) for x in range(length)]
        msg = reduce((lambda x, y: x + y), msg)
        for rate in range(1, 101, 25):
            for msg_count in range(100):
                # debug
                print(f'Sending message: {msg}, with error rate: {rate}')

                # send original message string
                s.sendall(msg.encode('UTF'))
                s.recv(1024)

                # send error rate
                s.sendall(bytes([rate]))
                s.recv(1024)
                
                # encode and send using Hamming
                encoder.encode(data=msg)
                encoder.add_noise(rate=rate)
                s.sendall(encoder.hamming_encoded.tobytes())
                s.recv(1024)
                
                # encode and send using Fletcher
                s.sendall(add_noise(encode(msg), rate).tobytes())
                s.recv(1024)
    s.sendall(b'END')