import socket
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from bitarray import bitarray
from hamming import Hamming
from fletcher import *

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 6969        # Port to listen on (non-privileged ports are > 1023)
PACKET_SIZE = 128
HAMMING = 1
FLETCHER = 2

ASCII = 'ascii'
UTF = 'latin-1'

# estadisticas
hamming_stats = {}
fletcher_stats = {}

decoder = Hamming()
msg_count = 0
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            errorDetection = 0

            # recv original message
            original_msg = conn.recv(PACKET_SIZE)
            original_msg = original_msg.decode(UTF)
            if original_msg == 'END':
                break
            conn.send(b'1')
            
            # recv error rate
            error_rate = conn.recv(PACKET_SIZE)
            error_rate = int.from_bytes(error_rate, 'big')
            conn.send(b'1')

            # recv encoded message
            data = conn.recv(PACKET_SIZE)
            # build bitarray from data
            b = bitarray()
            b.frombytes(data)

            # for stats
            length_key = len(original_msg)

            # decode hamming
            #Length correction
            if (len(b) % 12 != 0):
                b = b[:-4]
            #Flag variable
            errorDetection = decoder.error_count
            #Decode call
            decoder.decode(data=b)

            #### [0,0,0,0]
            # [0] original message equal to Hamming decoded
            # [1] original message not equal to Hamming decoded
            # [2] Error detection cont 
            # [3] Error detection cont faild

            if original_msg == decoder.hamming_decoded:
                if length_key not in hamming_stats:
                    hamming_stats[length_key] = {}
                    hamming_stats[length_key][error_rate] = [0, 0, 0, 0]
                if error_rate not in hamming_stats[length_key]:
                    hamming_stats[length_key][error_rate] = [0, 0, 0, 0]
                val = hamming_stats[length_key][error_rate]
                val[0] = val[0] + 1
            else:
                if length_key not in hamming_stats:
                    hamming_stats[length_key] = {}
                    hamming_stats[length_key][error_rate] = [0, 0, 0, 0]
                if error_rate not in hamming_stats[length_key]:
                    hamming_stats[length_key][error_rate] = [0, 0, 0, 0]
                val = hamming_stats[length_key][error_rate]
                val[1] = val[1] + 1
            #Detection error counter
            if (errorDetection != decoder.error_count):
                if length_key not in hamming_stats:
                    hamming_stats[length_key] = {}
                    hamming_stats[length_key][error_rate] = [0, 0, 0, 0]
                if error_rate not in hamming_stats[length_key]:
                    hamming_stats[length_key][error_rate] = [0, 0, 0, 0]
                val = hamming_stats[length_key][error_rate]
                val[2] = val[2] + 1
            else:
                if length_key not in hamming_stats:
                    hamming_stats[length_key] = {}
                    hamming_stats[length_key][error_rate] = [0, 0, 0, 0]
                if error_rate not in hamming_stats[length_key]:
                    hamming_stats[length_key][error_rate] = [0, 0, 0, 0]
                val = hamming_stats[length_key][error_rate]
                val[3] = val[3] + 1

            conn.send(b'1')

            # decode fletcher
            data = conn.recv(PACKET_SIZE)
            b = bitarray()
            b.frombytes(data)
            (fletcher_decoded, checksum_correct) = decode(b)

            #### [0,0,0,0]
            # [0] Checksum correct
            # [1] Checksum incorrect
            # [2] Checksum and message correct
            # [3] Checksum and message incorrect

            #Check for checksum
            if not checksum_correct:
                if length_key not in fletcher_stats:
                    fletcher_stats[length_key] = {}
                    fletcher_stats[length_key][error_rate] = [0, 0, 0, 0]
                if error_rate not in fletcher_stats[length_key]:
                    fletcher_stats[length_key][error_rate] = [0, 0, 0, 0]
                val = fletcher_stats[length_key][error_rate]
                val[0] = val[0] + 1
            else:
                if length_key not in fletcher_stats:
                    fletcher_stats[length_key] = {}
                    fletcher_stats[length_key][error_rate] = [0, 0, 0, 0]
                if error_rate not in fletcher_stats[length_key]:
                    fletcher_stats[length_key][error_rate] = [0, 0, 0, 0]
                val = fletcher_stats[length_key][error_rate]
                val[1] = val[1] + 1
            #Check for checksum, and incorrect message
            if (checksum_correct and (original_msg == decoder.hamming_decoded)):
                if length_key not in fletcher_stats:
                    fletcher_stats[length_key] = {}
                    fletcher_stats[length_key][error_rate] = [0, 0, 0, 0]
                if error_rate not in fletcher_stats[length_key]:
                    fletcher_stats[length_key][error_rate] = [0, 0, 0, 0]
                val = fletcher_stats[length_key][error_rate]
                val[0] = val[0] + 1
            else:
                if length_key not in fletcher_stats:
                    fletcher_stats[length_key] = {}
                    fletcher_stats[length_key][error_rate] = [0, 0, 0, 0]
                if error_rate not in fletcher_stats[length_key]:
                    fletcher_stats[length_key][error_rate] = [0, 0, 0, 0]
                val = fletcher_stats[length_key][error_rate]
                val[1] = val[1] + 1


            conn.send(b'1')
            msg_count = msg_count + 1
            print(f'Decoding message #{msg_count}')




# print statistics
print('Saving images of plots...')

def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

for length in hamming_stats.keys():
    labels = hamming_stats[length].keys()
    correct = []
    wrong = []
    for rate in hamming_stats[length]:
        val = hamming_stats[length][rate]
        correct.append(val[0])
        wrong.append(val[1])
    x = np.arange(len(labels))
    width = 0.35
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, correct, width, label='Corregido')
    rects2 = ax.bar(x + width / 2, wrong, width, label='No Corregido')
    ax.set_ylabel('Cantidad')
    ax.set_xlabel('Probabilidad de Error')
    ax.set_title(f'Hamming - Cantidad de Caracteres en Mensaje: {length}')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    autolabel(rects1)
    autolabel(rects2)
    fig.tight_layout()
    fig.savefig(f'./img/hamming_{length}.png')

for length in fletcher_stats.keys():
    labels = fletcher_stats[length].keys()
    correct = []
    wrong = []
    for rate in fletcher_stats[length]:
        val = fletcher_stats[length][rate]
        correct.append(val[0])
        wrong.append(val[1])
    x = np.arange(len(labels))
    width = 0.35
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, correct, width, label='Error Detectado')
    rects2 = ax.bar(x + width / 2, wrong, width, label='Mensajes sin Error')
    ax.set_ylabel('Cantidad')
    ax.set_xlabel('Cantidad de Errores de por cada 100 Bits')
    ax.set_title(f'Fletcher - Cantidad de Caracteres en Mensaje: {length}')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    autolabel(rects1)
    autolabel(rects2)
    fig.tight_layout()
    fig.savefig(f'./img/fletcher_{length}.png')

print('...done')
    
            