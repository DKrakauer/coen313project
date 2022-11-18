
# Address logic for converting hex to binary
def convertHexToBinary(addr):
    scale = 16 ## equals to hexadecimal
    num_of_bits = len(addr)*4
    return bin(int(addr, scale))[2:].zfill(num_of_bits)

def convertBinaryToDecimal(addr):
    return int(addr, 2)