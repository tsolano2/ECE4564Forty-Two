from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from clientKeys import*
from cryptography.fernet import Fernet
import socket, pickle
import sys
import json
import hashlib
import ipaddress

SERVER_IP = ""
SERVER_PORT = ""
SOCKET_SIZE = ""
HASHTAG = ""
if sys.argv[1] == "-s": #This section parses the command line and catches exceptions
    SERVER_IP = sys.argv[2]
    if sys.argv[3] == "-p":
        SERVER_PORT = sys.argv[4]
        if sys.argv[5] == "-z":
            SOCKET_SIZE = sys.argv[6]
            if sys.argv[7] == "-t":
                HASHTAG = sys.argv[8]
            else:
                raise Exception("Hashtag in line is INVALID")
        else:
            raise Exception("Socket size in argument line is INVALID")
    else:
        raise Exception("Port in argument line is INVALID")
else:
    raise Exception("Ip in argument line is INVALID")


print("[Checkpoint] Listening for Tweets that contain: " + HASHTAG)

question = ""
text = ""
key = ""

#From tweepy tutorial 
class listener(StreamListener):
<<<<<<< HEAD
    def on_status(self, status): 
        text = status.text  #gets the tweet from twitter
        user = status.user.screen_name  #gets the screen name
        question = text.replace(HASHTAG, "") 
=======
    def on_status(self, status):
        #print(repr(status))
        text = status.text
        user = status.user.screen_name
        question = text.replace(HASHTAG, "")
>>>>>>> 421e8b56d4225254b5e7995cefbe00c2b09e5cac
        print("[Checkpoint] New Tweet: " + question + " | User: " + user)

        # Used from cryptography.io
        key = Fernet.generate_key() #generates the key
        f = Fernet(key)
        question_bytes = question.encode()
        token = f.encrypt(question_bytes)
        offset = 5
        print("[Checkpoint] Encrypt: Generater Key: " + key.decode("utf-8")
              + " | Ciphertext: " + token.decode("utf-8"))

        hash_object = hashlib.md5(token)
        print("[Checkpoint] Generated MD5 Checksum: " + hash_object.hexdigest())

        tup = (key, token, hash_object.hexdigest())
        print("[Checkpoint] Connecting to " + SERVER_IP + " on port " + SERVER_PORT)
        
        #from stack overflow
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((SERVER_IP, int(SERVER_PORT)))
        payload = pickle.dumps(tup)
        tempTup = str(tup)
        print('[Checkpoint] Sending data: ' + tempTup)
        s.send(payload)
        info = s.recv(int(SOCKET_SIZE))
        s.close()
        
        #Loads information
        (answerEncrypt, answerCheckSum ) = pickle.loads(info)
<<<<<<< HEAD
=======
        #answerEncrypt = tempTup[0]
        #answerCheckSum = tempTup[1]
>>>>>>> 421e8b56d4225254b5e7995cefbe00c2b09e5cac
        checkHash = hashlib.md5(answerEncrypt)
        
        print("[Checkpoint] Received data: " + str(tempTup))
        checkHash = checkHash.hexdigest();
        answerCheckSum = str(answerCheckSum);
        if  answerCheckSum == checkHash:
            print("[Checkpoint] Checksum is VALID")
            decrypt = f.decrypt(answerEncrypt)
            print("[Checkpoint] Decrypt: Using Key " + answerEncrypt.decode("utf-8") + " | Plaintext: " + decrypt.decode("utf-8"))            
        else:
            raise Exception("[Checkpoint] Checksum is INVALID") #catches error if the checksum is invalid

        return True
    def on_error(self, status):
        print(status)
    def get_tweet(self, tweet):
        print(tweet.text);

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
twitterStream = Stream(auth, listener())
twitterStream.filter(track = [HASHTAG])
