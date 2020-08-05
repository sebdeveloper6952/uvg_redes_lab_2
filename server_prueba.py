import socket
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from bitarray import bitarray
from hamming import Hamming
import fletcher

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 6969        # Port to listen on (non-privileged ports are > 1023)
PACKET_SIZE = 128
HAMMING = 1
FLETCHER = 2

# estadisticas
stats = {}

decoder = Hamming()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            # recv original message
            original_msg = conn.recv(PACKET_SIZE)
            original_msg = original_msg.decode('ascii')
            if original_msg == 'END':
                break
            conn.send(b'1')
            
            # recv error rate
            error_rate = conn.recv(PACKET_SIZE)
            error_rate = int.from_bytes(error_rate, 'big')
            conn.send(b'1')

            # recv message type
            data = conn.recv(PACKET_SIZE)
            msg_type = int.from_bytes(data, 'big')
            # send message type ack
            conn.send(b'1')

            # recv encoded message
            data = conn.recv(PACKET_SIZE)
            # build bitarray from data
            b = bitarray()
            b.frombytes(data)

            # for stats
            length_key = len(original_msg)

            # decode message depending on message type
            if msg_type == HAMMING:
                if (len(b) % 12 != 0):
                    b = b[:-4]
                decoder.decode(data=b)
                if original_msg == decoder.hamming_decoded:
                    if length_key not in stats:
                        stats[length_key] = {}
                        stats[length_key][error_rate] = [0, 0]
                    if error_rate not in stats[length_key]:
                        stats[length_key][error_rate] = [0, 0]
                    val = stats[length_key][error_rate]
                    val[0] = val[0] + 1
                else:
                    if length_key not in stats:
                        stats[length_key] = {}
                        stats[length_key][error_rate] = [0, 0]
                    if error_rate not in stats[length_key]:
                        stats[length_key][error_rate] = [0, 0]
                    val = stats[length_key][error_rate]
                    val[1] = val[1] + 1
            else:
                print('Message type is fletcher.')
            # send decoded ack
            conn.send(b'1')

# print statistics
print('Saving images of plots...')
for length in stats.keys():
    labels = stats[length].keys()
    correct = []
    wrong = []
    for rate in stats[length]:
        # print(f'({length}, {rate}) => {stats[length][rate]}')
        val = stats[length][rate]
        correct.append(val[0])
        wrong.append(val[1])
    # print(f'Make fig for length {length}')
    x = np.arange(len(labels))
    width = 0.35
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, correct, width, label='Corregido')
    rects2 = ax.bar(x + width/2, wrong, width, label='No Corregido')
    ax.set_ylabel('Cantidad')
    ax.set_xlabel('Probabilidad de Error')
    ax.set_title(f'Hamming - Cantidad de Caracteres en Mensaje: {length}')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
    autolabel(rects1)
    autolabel(rects2)
    fig.tight_layout()
    fig.savefig(f'./img/hamming_{length}.png')
print('...done')
    
            