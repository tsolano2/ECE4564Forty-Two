import argparse
import socket
from cryptography.fernet import Fernet
import hashlib
import sys
#import serverKeys
import wolframalpha
import pickle




    ##########################################Initialization Phase####################################################

serverPort = int(sys.argv[2])

backLog = int(sys.argv[4])

serverSize = int(sys.argv[6])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

m = hashlib.md5()

#wolframClient = wolframalpha.Client(wolfram_alpha_appid)

s.bind(('0.0.0.0',serverPort))

print('[Checkpoint] Created Socket at 0.0.0.0 on port '+str(serverPort)) #first checkPoint

s.listen(backLog)

print('[Checkpoint] Listening for client connections!')

      ############################################ProcessServerRequest########################################################
while 1:

    client, address = s.accept()
    addressString = str(address)
    print('[Checkpoint] Accepted client connection from '+addressString+' at port '+str(serverPort))

    data = client.recv(serverSize)
    stringData = str(data)
    print('[Checkpoint] Received: '+stringData)

    (key, encryptedQuestion, md5Hash) = data

    f = Fernet(key)

    m.update(encryptedQuestion)

    plainQuestion = f.decrypt(encryptedQuestion)

    checkHash = m.digest()

    if(checkHash==md5Hash):
        print('[Checkpoint] Checksum is VALID')
        print('[Checkpoint] Decrypt using key '+str(key)+' | plaintext = '+plainQuestion)
        print('[Checkpoint] Speaking Question: '+plainQuestion)
        #speak through GTTS
        print('[Checkpoint] Sending question to Wolfram Alpha: '+plainQuestion)
        #plainAnswer = wolframClient.query(plainQuestion)
        #print('Checkpoint] Recieved answer from Wolframalpha: '+plainAnswer)
        #encryptedAnswer = f.encrypt(plainAnswer)
        #print('[Checkpoint] Encrypt: Generate key: '+key+' | Ciphertext: '+encryptedAnswer)
        #m.update(encryptedAnswer)
        #checkHash = m.digest()
        #print('[Checkpoint] MD5 Checksum: '+checkHash)
        #
    else:
        print('[Checkpoint] Checksum is INVALID')
