import socket
from hamming import Hamming

# hostname servidor/receptor
HOST = '127.0.0.1'
# puerto de servidor/receptor
PORT = 6969
# probabilidad de ruido: 1 error cada 100 bits
NOISE_RATE = 50
# para reproducibilidad
RANDOM_SEED = 5000
# ****************************************** HAMMING *********************************************
# CAPA: APLICACION
msg = 'ola amigo!'
# CAPA: VERIFICACION
hamming_encoder = Hamming(data=msg, random_seed=RANDOM_SEED)
hamming_encoder.encode()
print(f'Codificado: {hamming_encoder.hamming_encoded}')

# CAPA: AGREGAR RUIDO
hamming_encoder.add_noise(rate=NOISE_RATE)
print(f'Se agregaron {hamming_encoder.noise_count} errores.')

# decodificacion
hamming_decoder = Hamming(binary=hamming_encoder.hamming_encoded)
hamming_decoder.decode(correct=False)
decoded = hamming_decoder.hamming_decoded
print(f'Decodificado: {decoded}, se corrigieron {hamming_decoder.error_count} errores.')
hamming_decoder.decode()
decoded = hamming_decoder.hamming_decoded
print(f'Decodificado: {decoded}, se corrigieron {hamming_decoder.error_count} errores.')

    
# CAPA: TRANSMISION
# socket.sendall(msg_bitarray.tobytes())

# el servidor lo recibe asi:
# data = socket.recv(1024)
# b = bitarray(endian='little')
# b.frombytes(data)

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.connect((HOST, PORT))
#     s.sendall(msg_bitarray.tobytes())