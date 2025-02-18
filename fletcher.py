from bitarray import bitarray
from bitstring import BitArray 
from random import randrange

ASCII = 'ascii'
UTF = 'latin-1'

def fletcher(message):
    sum1 = 0
    sum2 = 0
    for l in message:
      sum1 = (sum1 + ord(l)) % 255
      sum2 = (sum2 + sum1) % 255
    return (sum1, sum2)


def checkSumToBitArray(n1, n2):
    return ( bitarray(BitArray(uint= n1, length=8)) + bitarray(BitArray(uint= n2, length=8)) )


def encode(original_data):
  l = len(original_data)
  encoded = bitarray()
  encoded.frombytes(original_data.encode(UTF))
  return encoded + checkSumToBitArray(*fletcher(original_data))
        
def decode(recive_data):
  data = bitarray()
  reciveFletcher = bitarray()

  data = recive_data[:-16]
  message = data.tobytes().decode(UTF)
  
  confirmation = recive_data[-16:] 

  return (message, confirmation == checkSumToBitArray(*fletcher(message)))

def add_noise(encoded, rate=1):
  noise_count = 0
  for i in range(0, len(encoded)):
    p = randrange(100)
    if p < rate:
      noise_count = noise_count + 1
      encoded[i] = not encoded[i]
    
  return encoded
     