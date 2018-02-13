from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from clientKeys import*
from cryptography.fernet import Fernet
import socket
import sys
import json
import hashlib

if sys.argv[1] == "-s":
    SERVER_IP = sys.argv[2]
    if sys.argv[3] == "-p":
        SERVER_PORT = sys.argv[4]
        if sys.argv[5] == "-z":
            SOCKET_SIZE = sys.argv[6]
            if sys.argv[7] == "-t":
                HASHTAG = sys.argv[8]

format_args = {SERVER_IP, SERVER_PORT, SOCKET_SIZE, HASHTAG}
print("[Checkpoint] Listening for Tweets that contain: " + HASHTAG)

question = ""
text = ""
#From tweepy tutorial
class listener(StreamListener):
    def on_data(self, data):
        text = json.loads(data)["text"]
        question = text.replace(HASHTAG + ' ', "")
        print(question)
        # Used from cryptography.io
        key = Fernet.generate_key
        f = Fernet(key)
        question_bytes = question.encode()
        token = f.encrypt(question_bytes)
        print("Here is the encrypted token: " + token)
       # hash_object = hashlib.md5(question_bytes)
       # print("\nHere is the md5 checksum: " + hash_object)
        return True
    def on_error(self, status):
        print(status)
    def get_tweet(self, tweet):
        print(tweet.text);

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
twitterStream = Stream(auth, listener())
twitterStream.filter(track = [HASHTAG])


