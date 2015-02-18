from Crypto.Hash import SHA256
from functools import partial

blocks = []

with open('6 - 1 - Introduction (11 min).mp4', 'rb') as openfileobject:
    for chunk in iter(partial(openfileobject.read, 1024), ''):
        blocks.append(chunk)

res = ""
blocks.reverse()

for block in blocks:
    res = SHA256.new(block + res).digest()

print res.encode('hex')