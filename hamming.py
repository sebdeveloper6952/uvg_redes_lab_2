from bitarray import bitarray
from random import seed, choice, randrange

class Hamming:
    def __init__(self, data=None, binary=None, random_seed=1):
        self.original_data = data
        self.hamming_encoded = binary
        self.error_count = 0
        self.noise_count = 0
        seed(random_seed)

    def encode(self, data=None):
        if data:
            self.original_data = data
        l = len(self.original_data)
        hamming = bitarray([False] * l * 12)
        for i in range(l):
            encoded = bitarray()
            encoded.frombytes(self.original_data[i].encode('ascii'))
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
        
        self.hamming_encoded = hamming

    def hamming_calculate_parity_bits(self, blockIndex):
        hamming = self.hamming_encoded[blockIndex:blockIndex + 12]
        old_parity_bits = bitarray([hamming[0], hamming[1], hamming[3], hamming[7]])
        hamming[0] = hamming[2] ^ hamming[4] ^ hamming[6] ^ hamming[8] ^ hamming[10]
        hamming[1] = hamming[2] ^ hamming[5] ^ hamming[6] ^ hamming[9] ^ hamming[10]
        hamming[3] = hamming[4] ^ hamming[5] ^ hamming[6] ^ hamming[11]
        hamming[7] = hamming[8] ^ hamming[9] ^ hamming[10] ^ hamming[11]
        new_parity_bits = bitarray([hamming[0], hamming[1], hamming[3], hamming[7]])

        self.hamming_encoded[blockIndex:blockIndex + 12] = hamming
        self.old_parity_bits = old_parity_bits
        self.new_parity_bits = new_parity_bits

        return (old_parity_bits, new_parity_bits)
    
    def decode(self, data=None, correct=True):
        if data:
            self.hamming_encoded = data
        if correct:
            self.error_count = 0

        data = bitarray()
        for i in range(0, len(self.hamming_encoded), 12):
            if correct:
                old, new = self.hamming_calculate_parity_bits(i)
                if old != new:
                    self.error_count = self.error_count + 1
                    a, sum = 1, 0
                    for j in range(4):
                        if old[j] != new[j]:
                            sum = sum + a
                        a = a << 1
                    sum = sum - 1
                    self.hamming_encoded[i + sum] = not self.hamming_encoded[i + sum]
            
            data.append(self.hamming_encoded[i + 2])
            data.append(self.hamming_encoded[i + 4])
            data.append(self.hamming_encoded[i + 5])
            data.append(self.hamming_encoded[i + 6])
            data.append(self.hamming_encoded[i + 8])
            data.append(self.hamming_encoded[i + 9])
            data.append(self.hamming_encoded[i + 10])
            data.append(self.hamming_encoded[i + 11])
        
        try:
            decoded = data.tobytes().decode('ascii')
            self.hamming_decoded = decoded
        except:
            pass
    
    def add_noise(self, rate=1):
        self.noise_count = 0
        options = [10, 11]
        for i in range(0, len(self.hamming_encoded), 12):
            p = randrange(100)
            if p < rate:
                self.noise_count = self.noise_count + 1
                self.hamming_encoded[i + 11] = not self.hamming_encoded[i + 11]
            p = randrange(100)
            if p < rate:
                self.noise_count = self.noise_count + 1
                self.hamming_encoded[i + 10] = not self.hamming_encoded[i + 10]