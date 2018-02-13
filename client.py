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
if sys.argv[1] == "-s":
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

# #adapted from code.sololearn.com
# alphabet = 'abcdefghijklmnopqrstuvwxyz'
# def encrypt(n, plaintext):
#     result  = ''
#     for l in plaintext:
#         try:
#             i = (alphabet.index(l) + n) % 26
#             result += alphabet[i]
#         except ValueError:
#             result += l
#     return result

#From tweepy tutorial
class listener(StreamListener):
    def on_status(self, status):
        print(repr(status))
        text = status.text
        user = status.user.screen_name
        question = text.replace(HASHTAG + ' ', "")
        print("[Checkpoint] New Tweet: " + text + " | User: " + user)

        # Used from cryptography.io
        key = Fernet.generate_key()
        #print("Here is the key: %i" (key.decode("utf-8")))
        f = Fernet(key)
        question_bytes = question.encode()
        token = f.encrypt(question_bytes)
        offset = 5
        print("[Checkpoint] Encrypt: Generater Key: " + key.decode("utf-8")
              + " | Ciphertext: " + token.decode("utf-8"))
        #print('Cyphertext: ', cypher_text)

        hash_object = hashlib.md5(token)
        print("[Checkpoint] Generated MD5 Checksum: " + hash_object.hexdigest())

        tup = (key, token, hash_object)
        print("[Checkpoint] Connecting to " + SERVER_IP + " on port " + SERVER_PORT)
        #from stack overflow
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((SERVER_IP, int(SERVER_PORT)))
        payload = pickle.dumps(tup)
        print("[Checkpoint] Sending data: %s" (tuple,))
        s.send(payload)
        info = s.recv(SOCKET_SIZE)
        s.close()
        print("[Checkpoint] Received data: ", repr(info))

        if info[2] == hash_object:
            print("[Checkpoint] Checksum is VALID")
            decrypt = f.decrypt(info[1])
            print("[Checkpoint] Decrypt: Using Key %s | Plaintext: %s" (info[0], decrypt))
        else:
            print("[Checkpoint] Checksum is INVALID")

        return True
    def on_error(self, status):
        print(status)
    def get_tweet(self, tweet):
        print(tweet.text);

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
twitterStream = Stream(auth, listener())
twitterStream.filter(track = [HASHTAG])
