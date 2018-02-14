import argparse
import socket
from cryptography.fernet import Fernet
import hashlib
import sys
import serverKeys
import wolframalpha
import pickle
from serverKeys import*




    ##########################################Initialization Phase####################################################

serverPort = int(sys.argv[2])

backLog = int(sys.argv[4])

serverSize = int(sys.argv[6])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


wolframClient = wolframalpha.Client(wolfram_alpha_appid)

s.bind(('0.0.0.0',serverPort))
    
print('[Checkpoint]: Created Socket at 0.0.0.0 on port '+str(serverPort)) #first checkPoint

s.listen(backLog)

print('[Checkpoint]: Listening for client connections!')

      ############################################ProcessServerRequest########################################################
while 1:
    
    client, address = s.accept()
    addressString = list(address)
    print('[Checkpoint]: Accepted client connection from '+addressString[0]+' at port '+str(serverPort))
    
    data = client.recv(serverSize)
    stringData = str(data)
    print('[Checkpoint]: Received: '+stringData)
    
    (key, encryptedQuestion, md5Hash) = pickle.loads(data)
    #print('Key: '+key)
    #print('EncryptedQuestion type: ')
    #print(type(encryptedQuestion))
    #print('md5 Hash type: ')
    #print(type(md5Hash))
    

    
    f = Fernet(key)

    key = str(key)
    #encryptedQuestion = str(encryptedQuestion)
    #encryptedQuestion = encryptedQuestion.encode()
    md5Hash = str(md5Hash)
    checkHash = hashlib.md5(encryptedQuestion)
   
    print('CheckHash type: ')
    print(type(checkHash))

    checkHash = checkHash.hexdigest()
    encryptedQuestion = encryptedQuestion.decode("utf-8")
    print('Encrypted Question: '+encryptedQuestion)
    print('md5 Hash of Question: '+md5Hash)
    print('Check hash: '+ checkHash)
    

    
    

    if(checkHash==md5Hash):
        plainQuestion = f.decrypt(encryptedQuestion.encode())
        print('[Checkpoint] Checksum is VALID')
        print('[Checkpoint] Decrypt using key '+key+' | plaintext = '+plainQuestion.decode("utf-8"))
        print('[Checkpoint] Speaking Question: '+plainQuestion.decode("utf-8"))
        #speak through GTTS
        print('[Checkpoint] Sending question to Wolfram Alpha: '+plainQuestion.decode("utf-8"))
        plainAnswer = wolframClient.query(plainQuestion)
        plainAnswer = plainAnswer.results
        
        print('Checkpoint] Recieved answer from Wolframalpha: '+plainAnswer)
        plainAnswer = plainAnswer.encode()
        encryptedAnswer = f.encrypt(plainAnswer)
        checkHash = hashlib.md5(encryptedAnswer)
        print('[Checkpoint] Encrypt: Generate key: '+key+' | Ciphertext: '+encryptedAnswer)
        print('[Checkpoint] MD5 Checksum: '+checkHash)
        payload = (encryptedAnswer, checkHash)
        pickle.dumps(payload)
        s.close()
    else:
        print('[Checkpoint] Checksum is INVALID')
    
    
    
    
    
    
    
    





    
            
    
    
    
    