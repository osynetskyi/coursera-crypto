import urllib2
import sys
import requests as rq

ct = "f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4"

net = rq.session()

TARGET = 'http://crypto-class.appspot.com/po?er='
#--------------------------------------------------------------
# padding oracle
#--------------------------------------------------------------
class PaddingOracle(object):
    '''def query(self, q):
        target = TARGET + urllib2.quote(q)    # Create query URL
        req = urllib2.Request(target)         # Send HTTP request to server
        try:
            f = urllib2.urlopen(req)          # Wait for response
        except urllib2.HTTPError, e:          
            print "We got: %d" % e.code       # Print response code
            if e.code == 404:
                return True # good padding
            return False # bad padding'''

    def query(self, q):
        #if q == ct:
        #    return True
        target = TARGET + q                         # Create query URL
        res = net.get(target)
        return res.status_code == 404

def form_pad(guess, pad):
    res = []
    for i in (0, pad):
        res.append(guess)
    return ''.join(res)

def dec2hex(num):
    res = hex(num).split('x')[1]
    if len(res) == 1:
        res = '0' + res
    return res

#print int(str(9) + '09', 16)

#print form_pad('02', 2)

#ct = "f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4"
chunks = ['f20bdba6ff29eed7b046d1df9fb70000', '58b1ffb4210a580f748b4ac714c001bd', '4a61044426fb515dad3f21f18aa577c0', 'bdf302936266926ff37dbf7035d5eeb4']

cur = chunks[2]
po = PaddingOracle()
#print po.query("f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4")
bytes_ = []
for i in range(0, len(cur)/2):
    bytes_.append(cur[2*i:2*(i+1)])

'''for guess in range(0, 255):
    byte = bytes_[-1]
    #print byte, guess,
    byte = hex((int(byte, 16) ^ guess )^ 1).split('x')[1]
    if len(byte) == 1:
        byte = "0" + byte
    guessed = ''.join(bytes_[:-1]) + byte
    send = chunks[0] + chunks[1] + guessed + chunks[3]
    if po.query(send):
        print "The correct guess is", guess'''
        
#correct = ['73', '69', '66', '72', '61', '67', '65','09', '09','09','09','09','09','09','09','09']
correct = []
                
for pad in range(1, 17):
    #print "padding is", dec2hex(pad)*pad
    for guess in range(0, 255):
        #print byte, guess,
        #print dec2hex(pad)*pad
        '''if len(correct) > 7:
            print "BOOM!", dec2hex(guess) + ''.join(correct)'''
        pwn = dec2hex(int(chunks[1], 16) ^ int(dec2hex(guess) + ''.join(correct), 16) ^ 
                  int(dec2hex(pad)*pad, 16))
        #guessed = ''.join(bytes_[:-1]) + byte
        send = chunks[0] + pwn[:-1] + chunks[2]
        print "Sending", pwn[:-1], 
        if po.query(send):
            print "\nThe correct guess is", guess
            correct.insert(0, dec2hex(guess))
            print "correct is now", ''.join(correct), "\n"
            break
            
'''for guess in range(0, 255):
    #print byte, guess,
    #print dec2hex(pad)*pad
    pwn = hex((int(chunks[2], 16) ^ int((dec2hex(guess) + '0909090909090909'), 16) ^ 
               int('090909090909090909', 16))).split('x')[1]
    #guessed = ''.join(bytes_[:-1]) + byte
    send = chunks[0] + chunks[1] + pwn[:-1] + chunks[3]
    #print send
    if po.query(send):
        print "The correct guess is", guess
        #correct.insert(0, dec2hex(guess))
        #print "correct is now", ''.join(correct)
        break'''
        