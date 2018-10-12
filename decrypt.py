
import sys
from BitVector import * #(A)

PassPhrase = "Hopes and dreams of a million years" #(C)
BLOCKSIZE = 16


numbytes = BLOCKSIZE // 8 #(E)
# Reduce the passphrase to a bit array of size BLOCKSIZE:
bv_iv = BitVector(bitlist = [0]*BLOCKSIZE) #(F)
for i in range(0,len(PassPhrase) // numbytes): #(G)
    textstr = PassPhrase[i*numbytes:(i+1)*numbytes] #(H)
    bv_iv ^= BitVector( textstring = textstr ) #(I)
print(bv_iv)
# Create a bitvector from the ciphertext hex string:
FILEIN = open("inDecryptText.txt") #(J)
encrypted_bv = BitVector( hexstring = FILEIN.read() ) #(K)
print(encrypted_bv)
# Get key from user:
key = None
if sys.version_info[0] == 3: #(L)
    key = input("\nEnter key: ") #(M)
else:
    key = raw_input("\nEnter key: ") #(N)
key = key.strip() #(O)
print(key)
# Reduce the key to a bit array of size BLOCKSIZE:
key_bv = BitVector(bitlist = [0]*BLOCKSIZE) #(P)
print(key_bv)
for i in range(0,len(key) // numbytes): #(Q)
    keyblock = key[i*numbytes:(i+1)*numbytes] #(R)
    key_bv ^= BitVector( textstring = keyblock ) #(S)
print(key_bv)
# Create a bitvector for storing the decrypted plaintext bit array:
msg_decrypted_bv = BitVector( size = 0 ) #(T)
# Carry out differential XORing of bit blocks and decryption:
previous_decrypted_block = bv_iv #(U)
for i in range(0, len(encrypted_bv) // BLOCKSIZE): #(V)
    bv = encrypted_bv[i*BLOCKSIZE:(i+1)*BLOCKSIZE] #(W)
    temp = bv.deep_copy() #(X)
    bv ^= previous_decrypted_block #(Y)
    previous_decrypted_block = temp #(Z)
    bv ^= key_bv #(a)
    msg_decrypted_bv += bv #(b)
# Extract plaintext from the decrypted bitvector:
outputtext = msg_decrypted_bv.get_text_from_bitvector() #(c)
# Write plaintext to the output file:
FILEOUT = open("outDecryptText.txt", 'w') #(d)
FILEOUT.write(outputtext) #(e)
FILEOUT.close()
