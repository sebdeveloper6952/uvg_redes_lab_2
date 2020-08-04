from bitarray import bitarray
from bitstring import BitArray

def fletcher(message):
    sum1 = 0
    sum2 = 0
    for l in message:
      sum1 = (sum1 + ord(l)) % 255
      sum2 = (sum2 + sum1) % 255
    return (sum1, sum2)


def checkSumToBitArray(n1, n2):
    return ( bitarray(BitArray(uint= n1, length=8)) + bitarray(BitArray(uint= n2, length=8)) )
