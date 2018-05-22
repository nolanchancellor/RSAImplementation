from random import randint


# Module 1: Key Setup
'''
Key Setup Consists of 6 functions, keys(), generate_prime(), primality(), mod_exponent(), and extended_euclid()
The module generates the public and private keys used to encrypt and decrypt files using RSA encryption.
Both keys are output to individual files, public_key and private_key
'''

'''
keys() gets two primes p and q and calculates the public key (n=p*q, e) with e being coprime with (p-1)*(q-1),
and the private key d, multiplicative inverse of e mod (p-1)*(q-1).
e is default set to 2^16 + 1, as this number is a sufficiently large prime number, so only multiples of
it will be coprime with it.
Writes the keys to files public_key and private_key
'''
def keys():
    # Generate 2 primes
    p = generate_prime()
    q = generate_prime()
    # Ensure that q and p are not equal
    while q == p:
        q = generate_prime()
    
    # Public key (n,e)    
    n = p*q
    e = 65537
    # Check if e mod (p-1)*(q-1) has a multiplicative inverse
    gcd = extended_euclid((p-1)*(q-1), e)[1]
    # If not, generate an e that does.
    while gcd != 1:
        e = randint(3, 10**5)
        gcd = extended_euclid((p-1)*(q-1), e)[1]
    
    # Public key for encryption
    publicKey = (n,e)
    # Private key for decryption
    # Multiplicative inverse of e mod (p-1)*(q-1)
    privateKey = extended_euclid((p-1)*(q-1), e)[0]
    
    # Write them to files delimited by spaces
    fPublic = open('public_key', 'w')
    fPublic.write(str(publicKey[0]) + ' ' + str(publicKey[1]))
    fPublic.close()
    
    fPrivate = open('private_key', 'w')
    fPrivate.write(str(privateKey))
    fPrivate.close()
    return

'''
generate_prime() generates a 100 digit number until the results of a primality test on it,
return prime.
'''
def generate_prime():
    # Random 100 digit number
    largeNum = randint(10**99, (10**100)-1)
    while not primality(largeNum):
        largeNum = randint(10**99, (10**100)-1)
    return largeNum

'''
primality() tests an input number for primality using repeated application of Fermat's Primality Test
returns true if the number is probably prime, false if it is composite
'''
def primality(num):
    # Performs up to 100 applications of Fermat's Primality Test
    timesToTest, i = 100, 0
    isPrime = True
    # Loop until 100 tests are done or the number is found to be composite
    while i < timesToTest and isPrime:
        base = randint(2, num-2)
        if mod_exponent(base, num-1, num) != 1:
            # Number is composite
            isPrime = False
        i += 1
    return isPrime

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

'''
extended_euclid() performs the Extended Euclidean Algorithm on 2 input numbers
returns the gcd of the two and the multiplicative inverse of num2 mod num1 if it exists
'''
def extended_euclid(num1, num2):
    xCurr = 0
    xPrev = 1
    yCurr = 1
    yPrev = 0
    rCurr = num1
    rPrev = num2
    
    while rCurr != 0:
        quotient = rPrev // rCurr
        rTemp = rPrev
        rPrev = rCurr
        rCurr = rTemp - quotient*rCurr
        xTemp = xPrev
        xPrev = xCurr
        xCurr = xTemp - quotient*xCurr
        yTemp = yPrev
        yPrev = yCurr
        yCurr = yTemp - quotient*yCurr
    
    # Multiplicative inverse of num2 mod num1    
    multInverse = xPrev % num1
    # Final rPrev is the gcd of num1 and num2
    return (multInverse, rPrev)


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
main() is the first function called in the program, it calls each module and exits the program on return
'''
def main():
    # Key Setup
    keys()
    # Encryption
    encrypt()
    # Decryption
    decrypt()
            
    return

main()