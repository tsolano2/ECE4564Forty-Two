"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Team Memberes: Teriencio Solano II, Angel Isidanso, Marcello Balboa
Team 16
Professor: William Plymale
Due Date: 2/18/18
Description: This is a program to configure the 2nd Raspberry Pi
as a TCP server, that accepts pickled requests from the client Pi,
processes the key, question, and md5 checksum, passes the decrypted
question through a WolframAlpha API query and sends the encrypted
result and md5 checksum of the result back to the client. Pi. 
Honor Code: I have neither given nor recieved unathorized assistance
on this assignment.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""





from gtts import gTTS
import argparse
import socket
from cryptography.fernet import Fernet
import hashlib
import sys
import serverKeys
import wolframalpha
import pickle
import os
from serverKeys import*




    ##########################################Initialization Phase####################################################

serverPort = int(sys.argv[2])

backLog = int(sys.argv[4])

serverSize = int(sys.argv[6])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


s.bind(('0.0.0.0',serverPort))
    
print('[Checkpoint]: Created Socket at 0.0.0.0 on port '+str(serverPort)) #first checkPoint

s.listen(backLog)

print('[Checkpoint]: Listening for client connections!')

      ############################################ProcessServerRequest########################################################
while 1:
    
    wolframClient = wolframalpha.Client(wolfram_alpha_appid)
    
    client, address = s.accept()
    addressString = list(address)
    print('[Checkpoint] Accepted client connection from '+addressString[0]+' at port '+str(serverPort))
    
    data = client.recv(serverSize)
    stringData = str(data)
    print('[Checkpoint] Received: '+stringData)
    
    (key, encryptedQuestion, md5Hash) = pickle.loads(data)
    

    
    f = Fernet(key)

    key = str(key)
    #encryptedQuestion = str(encryptedQuestion)
    #encryptedQuestion = encryptedQuestion.encode()
    md5Hash = str(md5Hash)
    checkHash = hashlib.md5(encryptedQuestion)
   

    checkHash = checkHash.hexdigest()
    encryptedQuestion = encryptedQuestion.decode("utf-8")
    print('Encrypted Question: '+encryptedQuestion)
    print('md5 Hash of Question: '+md5Hash)
    print('Check hash: '+ checkHash)
    

    
    

    if(checkHash==md5Hash):
        plainQuestion = f.decrypt(encryptedQuestion.encode())
        print('[Checkpoint] Checksum is VALID')
        print('[Checkpoint] Decrypt using key '+key+' | plaintext = '+plainQuestion.decode("utf-8"))
        print('[Checkpoint] Speaking Question: '+ plainQuestion.decode("utf-8"))
        #speak through GTTS
        tts = gTTS(text = plainQuestion.decode("utf-8"), lang='en')
        tts.save("temp.mp3")
        os.system("omxplayer temp.mp3")
        print('[Checkpoint] Sending question to Wolfram Alpha: '+plainQuestion.decode("utf-8"))
        plainAnswer = wolframClient.query(plainQuestion)
        try: 
            plainResult = next(plainAnswer.results).text
            print('[Checkpoint] Answer from wolfram alpha: '+plainResult)
        except StopIteration:
            print('No Results found :/')
        plainResult = plainResult.encode()
        encryptedAnswer = f.encrypt(plainResult)
        checkHash = hashlib.md5(encryptedAnswer).hexdigest()
        print('[Checkpoint] Encrypt: Generate key: '+key+' | Ciphertext: '+str(encryptedAnswer))
        print('[Checkpoint] MD5 Checksum: '+checkHash)
        payload = (encryptedAnswer, checkHash)
        payload = pickle.dumps(payload)
        client.send(payload)
        client.close()
    else:
        print('[Checkpoint] Checksum is INVALID')
    
    
    
    
    
    
    
    





    
            
    
    
    
    