#-*- coding: utf-8 -*-
# chcp 65001
import os
os.system('chcp 65001')

import tweepy as tw
import time, sys, socket

#my own module including Twitter keys
import my_tw_keys as conf 

consumer_key=conf.consumer_key
consumer_secret=conf.consumer_secret
access_token=conf.access_token
access_token_secret=conf.access_token_secret

#authentication
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)


port=9999
host='localhost'
conn = None
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)
print("Waiting for TCP connection...")
conn, addr = s.accept()
print("Connected... Starting getting tweets.")


class MyStreamListener(tw.StreamListener):

    def on_status(self, status):
        conn.send(status.text.encode("utf-8"))
        print(str(status._json.get("text")))
        # print(str(status._json.get("timestamp_ms")))
           

myStreamListener = MyStreamListener()
myStream = tw.Stream(auth = api.auth, listener=myStreamListener)
myStream.filter(track=['python'], encoding='utf8')
