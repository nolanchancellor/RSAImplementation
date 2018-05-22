# Module 3: Decryption
'''
Decryption consists of 3 functions, decrypt(), decode(), and mod_exponent()
Reads the public key, private key, and ciphertext from their files and decrypts and decodes
the ciphertext, writing the resulting plaintext in a file
'''

'''
decode() takes an input encoding and performs the compliment computations to get a string
Cannot decode NULL characters
returns the string after being decoded
'''
def decode(encoding):
    message = ''
    i = 0
    # First character 
    charEncode = ((encoding % 256**(i+1)) - (encoding % 256**i)) / 256**i
    # Check if each character encoding is NULL, if it is, exit loop
    while charEncode != 0:
        # ASCII character decoding
        message += chr(charEncode)
        i += 1
        # ith character 
        charEncode = ((encoding % 256**(i+1)) - (encoding % 256**i)) / 256**i
        
    return message

'''
decrypt() reads the ciphertext and public and private keys from their files and uses n (from the public
key) and the private key to get the plaintext
Writes the plaintext to a file called decrypted_message
'''
def decrypt():
    fPublic = open('public_key', 'r')
    publicKey = fPublic.read()
    fPublic.close()
    # File is space delimited for easy parsing
    publicKey = publicKey.split(' ')
    
    fPrivate = open('private_key', 'r')
    privateKey = fPrivate.read()
    fPrivate.close()
    
    fCiphertext = open('ciphertext', 'r')
    ciphertextList = fCiphertext.read()
    fCiphertext.close()
    # Space delimited again
    ciphertextList = ciphertextList.split(' ')
    
    decrypted = []
    decoding = ''
    # Decrypt each block of ciphertext c using the formula m = c^d mod n 
    for i in range(0, len(ciphertextList)):
        decrypted.append(mod_exponent(long(ciphertextList[i]), long(privateKey), long(publicKey[0])))
    
    # Decode each block of the decrypted ciphertext, appending them into a single string
    for i in range(0, len(decrypted)):
        decoding += decode(decrypted[i])
    
    fDecrypted = open('decrypted_message', 'w')
    fDecrypted.write(decoding)
    fDecrypted.close()
    
    return

'''
mod_exponent() performs modular exponentiation using an input base, exponent, and modulus
returns base^exponent mod (mod)
'''
def mod_exponent(base, exponent, mod):
    # Exponent must be in binary for algorithm
    binExponent = bin(exponent)
    result = 1
    
    while exponent > 0:
        # If a bit in the exponent is 1, calculate result*base mod (mod)
        if exponent % 2 == 1:
            result = (result*base) % mod
        # Shifting the exponent to get the next bit
        exponent = exponent >> 1
        # Squaring the base
        base = base**2 % mod
        
    return result

def main():
    # Begin decryption
    decrypt()
    return

main()