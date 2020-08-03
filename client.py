import socket
from bitarray import bitarray
from random import randrange
from random import seed, choice
from hamming import Hamming

# hostname servidor/receptor
HOST = '127.0.0.1'
# puerto de servidor/receptor
PORT = 6969
# probabilidad de ruido: 1 error cada 100 bits
NOISE_RATE = 50
# para reproducibilidad
RANDOM_SEED = 5000
# aplicar seed para random
seed(RANDOM_SEED)

def hamming_encode(string):
    hamming = bitarray([False] * (len(string) * 12))
    for i in range(len(string)):
        encoded = bitarray()
        encoded.frombytes(string[i].encode('ascii'))
        offset = i * 12
        hamming[offset + 2] = encoded[0]
        hamming[offset + 4] = encoded[1]
        hamming[offset + 5] = encoded[2]
        hamming[offset + 6] = encoded[3]
        hamming[offset + 8] = encoded[4]
        hamming[offset + 9] = encoded[5]
        hamming[offset + 10] = encoded[6]
        hamming[offset + 11] = encoded[7]
        hamming[offset + 0] = hamming[offset + 2] ^ hamming[offset + 4] ^ hamming[offset + 6] ^ hamming[offset + 8] ^ hamming[offset + 10]
        hamming[offset + 1] = hamming[offset + 2] ^ hamming[offset + 5] ^ hamming[offset + 6] ^ hamming[offset + 9] ^ hamming[offset + 10]
        hamming[offset + 3] = hamming[offset + 4] ^ hamming[offset + 5] ^ hamming[offset + 6] ^ hamming[offset + 11]
        hamming[offset + 7] = hamming[offset + 8] ^ hamming[offset + 9] ^ hamming[offset + 10] ^ hamming[offset + 11]
    
    return hamming

def hamming_calculate_parity_bits(hamming):
    old_parity_bits = bitarray([hamming[0], hamming[1], hamming[3], hamming[7]])
    hamming[0] = hamming[2] ^ hamming[4] ^ hamming[6] ^ hamming[8] ^ hamming[10]
    hamming[1] = hamming[2] ^ hamming[5] ^ hamming[6] ^ hamming[9] ^ hamming[10]
    hamming[3] = hamming[4] ^ hamming[5] ^ hamming[6] ^ hamming[11]
    hamming[7] = hamming[8] ^ hamming[9] ^ hamming[10] ^ hamming[11]
    new_parity_bits = bitarray([hamming[0], hamming[1], hamming[3], hamming[7]])
    
    return (old_parity_bits, new_parity_bits)

# Decodifica un array de bits a cadena de caracteres ascii,
# aplicando correccion si es necesario.
def hamming_decode(binary, correct=True):
    data = bitarray()
    for i in range(0, len(binary), 12):
        old, new = hamming_calculate_parity_bits(bitarray(binary[i:i + 12]))
        
        if correct and (old != new):
            a, sum = 1, 0
            for j in range(4):
                if old[j] != new[j]:
                    sum = sum + a
                a = a << 1
            binary[i + (sum - 1)] = not binary[i + (sum - 1)]
        data.append(binary[i + 2])
        data.append(binary[i + 4])
        data.append(binary[i + 5])
        data.append(binary[i + 6])
        data.append(binary[i + 8])
        data.append(binary[i + 9])
        data.append(binary[i + 10])
        data.append(binary[i + 11])
    
    return data.tobytes().decode('ascii')
    


# CAPA: APLICACION
msg = 'ola amigo!'
# CAPA: VERIFICACION
hamming_encoded = hamming_encode(msg)

# CAPA: AGREGAR RUIDO
options = [2, 4, 5, 6, 7, 8, 9, 10, 11]
for i in range(0, len(hamming_encoded), 12):
    p = randrange(100)
    if p < NOISE_RATE:
        c = choice(options)
        hamming_encoded[i + c] = not hamming_encoded[i + c]

# decodificacion
hamming_with_noise = hamming_decode(hamming_encoded, correct=False)
hamming_decoded = hamming_decode(hamming_encoded)
print(f'With noise: {hamming_with_noise}')
print(f'Corrected: {hamming_decoded}')

    
# CAPA: TRANSMISION
# socket.sendall(msg_bitarray.tobytes())

# el servidor lo recibe asi:
# data = socket.recv(1024)
# b = bitarray(endian='little')
# b.frombytes(data)

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.connect((HOST, PORT))
#     s.sendall(msg_bitarray.tobytes())