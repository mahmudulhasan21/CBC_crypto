
import sys
#from BitVector import * #(A)

PassPhrase = "Hopes and dreams of a million years" #(C)
BLOCKSIZE = 16


numbytes = BLOCKSIZE // 8 #(E)
# Reduce the passphrase to a bit array of size BLOCKSIZE:
#bv_iv = BitVector(bitlist = [0]*BLOCKSIZE) #(F)

#change : take empty bv_iv
bv_iv = "0000000000000000"
#print(bv_iv)
for i in range(0,len(PassPhrase) // numbytes): #(G)
    #change : take manually input string to build bv_iv
    textstr = PassPhrase[i*numbytes]+PassPhrase[(i*numbytes)+1] #(H)
    #change : convert into 8-bit binary
    textBinary =''.join('{0:08b}'.format(ord(x), 'b') for x in textstr)
    #print(i)
    #print(textBinary)
    #bv_iv ^= BitVector( textstring = textstr ) #(I)
    tempOne = bv_iv
    #print(tempOne)
    tempTwo = int(tempOne,2) ^ int(textBinary,2)
    #change : convert into 8-bit binary keeping leading zero
    bv_iv = bin(tempTwo)[2:].zfill(len(tempOne))
    #print(bv_iv)
print("bv_iv: "+bv_iv)
print(" ")
# Create a bitvector from the ciphertext hex string:
FILEIN = open("inDecryptText.txt") #(J)
#encrypted_bv = BitVector( hexstring = FILEIN.read() ) #(K)

#change : take input from the input.text file
hexstring = FILEIN.read()
print("cipher text :")
print(hexstring)
print(" ")
scale = 16
num_of_bits = 4
encrypted_bv = ""
#change : take each hex and convert it into 4-bit binary
for ch in hexstring:
    encrypted_bv = encrypted_bv + bin(int(ch, scale))[2:].zfill(num_of_bits)
    
#print (encrypted_bv)

# Get key from user:
#key = None
#if sys.version_info[0] == 3: #(L)
#    key = input("\nEnter key: ") #(M)
#else:
#    key = raw_input("\nEnter key: ") #(N)
#key = key.strip() #(O)
# Reduce the key to a bit array of size BLOCKSIZE:
#key_bv = BitVector(bitlist = [0]*BLOCKSIZE) #(P)
#for i in range(0,len(key) // numbytes): #(Q)
#    keyblock = key[i*numbytes:(i+1)*numbytes] #(R)
#    key_bv ^= BitVector( textstring = keyblock ) #(S)

for ii in range(2**16):
    #key_bv = BitVector(intVal=ii, size=16)
    #change : key generation
    a = "0000000000000000"
    b = ii
    key_bv = bin(b)[2:].zfill(len(a))
    #print(key_bv)
    # Create a bitvector for storing the decrypted plaintext bit array:
    #msg_decrypted_bv = BitVector( size = 0 ) #(T)

    #change : take a empty space
    msg_decrypted_bv  = ""
    
    # Carry out differential XORing of bit blocks and decryption:
    previous_decrypted_block = bv_iv #(U)
    for i in range(0, len(encrypted_bv) // BLOCKSIZE): #(V)
        #bv = encrypted_bv[i*BLOCKSIZE:(i+1)*BLOCKSIZE] #(W)
        #change : manullay take bit from encrypted_bv
        bv = encrypted_bv[i*BLOCKSIZE]+encrypted_bv[i*BLOCKSIZE+1]+encrypted_bv[i*BLOCKSIZE+2]+encrypted_bv[i*BLOCKSIZE+3]
        bv = bv+encrypted_bv[i*BLOCKSIZE+4]+encrypted_bv[i*BLOCKSIZE+5]+encrypted_bv[i*BLOCKSIZE+6]+encrypted_bv[i*BLOCKSIZE+7]
        bv = bv+encrypted_bv[i*BLOCKSIZE+8]+encrypted_bv[i*BLOCKSIZE+9]+encrypted_bv[i*BLOCKSIZE+10]+encrypted_bv[i*BLOCKSIZE+11]
        bv = bv+encrypted_bv[i*BLOCKSIZE+12]+encrypted_bv[i*BLOCKSIZE+13]+encrypted_bv[i*BLOCKSIZE+14]+encrypted_bv[i*BLOCKSIZE+15]
        #print(i)
        #print(bv)
        #temp = bv.deep_copy() #(X)
        #change : copy previous bv
        temp = bv
        #bv ^= previous_decrypted_block #(Y)
        #change : xor with previous_decrypted_block 
        tempOne = bv
        tempTwo = int(tempOne,2) ^ int(previous_decrypted_block,2)
        #change : convert into 8-bit binary keeping leading zero
        bv = bin(tempTwo)[2:].zfill(len(tempOne))
        #print(bv)
        previous_decrypted_block = temp #(Z)
        #bv ^= key_bv #(a)
        #change : xor with key_bv
        tempOne = bv
        tempTwo = int(tempOne,2) ^ int(key_bv,2)
        #change : convert into 8-bit binary keeping leading zero
        bv = bin(tempTwo)[2:].zfill(len(tempOne))
        #print(bv)
        msg_decrypted_bv += bv #(b)

    #print("encrypted message in binary bit")
    #print(msg_decrypted_bv)
    # Extract plaintext from the decrypted bitvector:
    #outputtext = msg_decrypted_bv.get_text_from_bitvector() #(c)

    #change : output text create by converting binary into ascii char
    outputtext = ""
    length = len(msg_decrypted_bv)
    length = int(length/8)
    #print(length)
    for i in range(length):
        c = msg_decrypted_bv[i*8+0]+msg_decrypted_bv[i*8+1]+msg_decrypted_bv[i*8+2]+msg_decrypted_bv[i*8+3]
        c = c+msg_decrypted_bv[i*8+4]+msg_decrypted_bv[i*8+5]+msg_decrypted_bv[i*8+6]+msg_decrypted_bv[i*8+7]
        #print(c)
        n = int(c,2)
        #print(n)
        ch = chr(n)
        #print(ch)
        outputtext = outputtext+ch
    #print("output text")
    #print(outputtext)
    #print("")

    if "nowhere" in outputtext:
        print(key_bv)
        #print(key_bv.get_text_from_bitvector())
        #change : key create by converting binary into ascii char
        key = ""
        length = len(key_bv)
        length = int(length/8)
        for i in range(length):
            c = key_bv[i*8+0]+key_bv[i*8+1]+key_bv[i*8+2]+key_bv[i*8+3]
            c = c+key_bv[i*8+4]+key_bv[i*8+5]+key_bv[i*8+6]+key_bv[i*8+7]
            #print(c)
            n = int(c,2)
            #print(n)
            ch = chr(n)
            #print(ch)
            key = key+ch
        print("key : "+key)
        print("outputtext :")
        print(outputtext)
        # Write plaintext to the output file:
        FILEOUT = open("outTextCTattack.txt", 'w') #(d)
        FILEOUT.write(outputtext) #(e)
        FILEOUT.close
        break
    
    print(ii)
