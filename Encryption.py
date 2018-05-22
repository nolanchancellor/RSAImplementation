#!/usr/bin/env python


# Module 2: Encryption
'''
Encryption consists of 3 functions, encode(), encrypt(), and mod_exponent().
Reads from a plaintext file as well as the public key file and writes the ciphertext to a ciphertext file
'''

'''
encode() computes the encoding for an n length input message, n <= 82.
Uses the formula: encoding = m0 + m1*256 + m2*256^2 + ... + mk-1*256^k-1
returns the number encoding the message
'''
def encode(message):
    messageEncoding = 0
    for i in range(0,len(message)):
        # ASCII character encoding
        messageEncoding += ord(message[i]) * 256**i
    
    return messageEncoding
'''
encrypt() computes the encryption on the plaintext using the public key, both read from files
Gets the encoding of the plaintext before encrypting, as RSA encrypts on numbers
Writes the ciphertext to the file called ciphertext
'''
def encrypt():
    fKey = open('public_key', 'r')
    key = fKey.read()
    fKey.close()
    # File space delimited for easy parsing
    key = key.split(' ')
    
    fMessage = open('message', 'r')
    plaintext = fMessage.read()
    fMessage.close()
    
    # Total number of blocks of length at most 82 to be encoded
    numBlocks = len(plaintext)//82 + 1
    # Maximum block length
    maxLen = 82
    encoding, ciphertextList = [], []
    
    for i in range(0, numBlocks):
        if i < numBlocks:
            encoding.append(encode(plaintext[maxLen*i : maxLen*i + maxLen]))
        else:
            encoding.append(encode(plaintext[maxLen*i : ]))    
            
    for i in range(0, len(encoding)):
        ciphertextList.append(mod_exponent(encoding[i], long(key[1]), long(key[0])))
        
    fCiphertext = open('ciphertext', 'w')
    fCiphertext.write(str(ciphertextList[0]))
    for i in range(1, len(ciphertextList)):
        fCiphertext.write(' ' + str(ciphertextList[i]))
    fCiphertext.close()
    
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
    # Begin encryption
    encrypt()
    return

main()