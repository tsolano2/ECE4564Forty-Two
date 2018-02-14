import argparse
import socket
from cryptography.fernet import Fernet
import hashlib
import sys
import serverKeys
import wolframalpha
import pickle




    ##########################################Initialization Phase####################################################

serverPort = int(sys.argv[2])

backLog = int(sys.argv[4])

serverSize = int(sys.argv[6])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#client = wolframalpha.Client(wolfram_alpha_appid)

s.bind(('0.0.0.0',serverPort))
    
print('[Checkpoint]: Created Socket at 0.0.0.0 on port '+str(serverPort)) #first checkPoint

s.listen(backLog)

print('[Checkpoint]: Listening for client connections!')

      ############################################ProcessServerRequest########################################################
while 1:
    
    client, address = s.accept()
    addressString = str(address)
    print('[Checkpoint]: Accepted client connection from '+addressString+' at port '+str(serverPort))
    
    data = client.recv(serverSize)
    stringData = str(data)
    print('[Checkpoint]: Received: '+stringData)
    
    testTuple = ('answerText', 'md5Hash')
    sendData = pickle.dumps(testTuple)
    client.send(sendData)
    s.close()
    
    
    
    
    
    
    
    





    
            
    
    
    
    