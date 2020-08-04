from random import seed, randrange
import socket
from hamming import Hamming
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from functools import reduce

# data
#x_data = [x for x in range(100)]
#y_data = [x * 2 for x in range(100)]
#y_data_1 = [x * 3 for x in range(100)]
# line plot config
#fig, ax = plt.subplots()
#ax.plot(x_data, y_data, '#d8572a', label='Hamming')
#ax.plot(x_data, y_data_1, '#780116', label='CRC-32')
# ax.bar(['apple', 'orange'], [4, 10])
# ax.set(xlabel='X Label', ylabel='Y Label',
#        title=f'Desempeño para L={100}, N={5}')
#ax.grid()
# ax.legend()
#fig.savefig("test.png")
# show plot
# plt.show()

# bar plot
# labels = ['G1', 'G2', 'G3', 'G4', 'G5']
# men_means = [20, 34, 30, 35, 27]
# women_means = [25, 32, 34, 20, 25]
# x = np.arange(len(labels))  # the label locations
# width = 0.35  # the width of the bars
# fig, ax = plt.subplots()
# rects1 = ax.bar(x - width/2, men_means, width, label='Men')
# rects2 = ax.bar(x + width/2, women_means, width, label='Women')
# # Add some text for labels, title and custom x-axis tick labels, etc.
# ax.set_ylabel('Scores')
# ax.set_title('Scores by group and gender')
# ax.set_xticks(x)
# ax.set_xticklabels(labels)
# ax.legend()
# def autolabel(rects):
#     """Attach a text label above each bar in *rects*, displaying its height."""
#     for rect in rects:
#         height = rect.get_height()
#         ax.annotate('{}'.format(height),
#                     xy=(rect.get_x() + rect.get_width() / 2, height),
#                     xytext=(0, 3),  # 3 points vertical offset
#                     textcoords="offset points",
#                     ha='center', va='bottom')
# autolabel(rects1)
# autolabel(rects2)
# fig.tight_layout()
# plt.show()

# hostname servidor/receptor
HOST = '127.0.0.1'
# puerto de servidor/receptor
PORT = 6969
# para reproducibilidad
RANDOM_SEED = 5000
seed(RANDOM_SEED)
# ****************************************** HAMMING *********************************************
# CAPA: APLICACION
# msg = 'ola amigo!'
# # CAPA: VERIFICACION
# hamming_encoder = Hamming(data=msg, random_seed=RANDOM_SEED)
# hamming_encoder.encode()
# print(f'Codificado: {hamming_encoder.hamming_encoded}')

# # CAPA: AGREGAR RUIDO
# hamming_encoder.add_noise(rate=NOISE_RATE)
# print(f'Se agregaron {hamming_encoder.noise_count} errores.')

# # decodificacion
# hamming_decoder = Hamming(binary=hamming_encoder.hamming_encoded)
# hamming_decoder.decode(correct=False)
# decoded = hamming_decoder.hamming_decoded
# print(f'Decodificado: {decoded}, se corrigieron {hamming_decoder.error_count} errores.')
# hamming_decoder.decode()
# decoded = hamming_decoder.hamming_decoded
# print(f'Decodificado: {decoded}, se corrigieron {hamming_decoder.error_count} errores.')

    
# CAPA: TRANSMISION
# socket.sendall(msg_bitarray.tobytes())

# el servidor lo recibe asi:
# data = socket.recv(1024)
# b = bitarray(endian='little')
# b.frombytes(data)

encoder = Hamming()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print('Connected to server.')
    for length in range(1, 10):
        msg = [chr(randrange(97, 123)) for x in range(length)]
        msg = reduce((lambda x, y: x + y), msg)
        print(f'Sending message: {msg}')
        for rate in range(1, 100):
            encoder.encode(data=msg)
            encoder.add_noise(rate=rate)
            s.sendall(encoder.hamming_encoded.tobytes())
            s.recv(1024)
        