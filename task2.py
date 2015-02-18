# -*- coding: utf-8 -*-
from Crypto import Random
from Crypto.Cipher import AES

BLOCK_SIZE = 32

key = "140b41b22a29beb4061bda66b6747e14"
CT = "4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81"

CT2 = "5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253"

#CT = "69dda8455c7dd4254bf353b773304eec0ec7702330098ce7f7520d1cbbb20fc388d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f51eeca32eabedd9afa9329"
#key = "36f18357be4dbd77f050515c73fcf9f2"

#CT2 = "770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa0e311bde9d4e01726d3184c34451"
#key2 = "36f18357be4dbd77f050515c73fcf9f2"

#print CT.decode('hex')

def strxor(a, b):     # xor two strings of different lengths
    if len(a) > len(b):
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a[:len(b)], b)])
    else:
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b[:len(a)])])

def split(string):
    res = []
    for i in range(0, len(string), BLOCK_SIZE):
        res.append(string[i:i+BLOCK_SIZE])
    return res
    
def CTR_encrypt(key, msg):
    ct = []
    IV = Random.new().read(BLOCK_SIZE)
    initial_IV = IV
    msg_blocks = split(msg)
    cipher = AES.new(key.decode('hex'))
    for block in msg_blocks:
        session_key = cipher.encrypt(IV)
        ct.append(strxor(block.decode('hex'), session_key))
        ivl = list(IV)
        ivl[-1] = chr(ord(ivl[-1]) + 1)
        IV = "".join(ivl)
    return initial_IV + "".join(ct)
    
def CTR_decrypt(key, ct):
    msg = []
    ct_blocks = split(ct)
    IV = ct_blocks[0].decode('hex')
    cipher = AES.new(key.decode('hex'))
    for block in ct_blocks[1:]:
        session_key = cipher.encrypt(IV)
        msg.append(strxor(block.decode('hex'), session_key))
        ivl = list(IV)
        ivl[-1] = chr(ord(ivl[-1]) + 1)
        IV = "".join(ivl)
    return "".join(msg)
    
def pad(block):
    hexblock = block.encode('hex')
    count = (len(hexblock) % 32) / 2
    if count != 0:
        for i in range(0, count):
            hexblock += str(hex(count))[-2:]
    else:
        hexblock = "10"*16
    return hexblock.decode('hex')
        
#def unpad(block):
    #hexblock = block.encode('hex')
    #count = 

"""def CBC_encrypt(key, msg):
    ct = []
    IV = Random.new().read(BLOCK_SIZE)
    add = str(IV)
    msg_blocks = split(msg)
    cipher = AES.new(key.decode('hex'))
    for block in msg_blocks:
        cur = cipher.encrypt(strxor(block.decode('hex'), add))
        ct.append(cur)
        add = cur
    
    return ct
"""    
def CBC_decrypt(key, ct):
    msg = []
    ct_blocks = split(ct)
    IV = ct_blocks[0].decode('hex')
    add = IV
    cipher = AES.new(key.decode('hex'))
    for block in ct_blocks[1:]:
        msg.append(strxor(add, cipher.decrypt(block.decode('hex'))))
        add = block.decode('hex')
    return "".join(msg)
    
print CBC_decrypt(key, CT)
print CBC_decrypt(key, CT2)