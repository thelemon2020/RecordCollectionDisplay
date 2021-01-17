import tkinter as tk
import json
import sys
import RecordCollectionDisplay
import webbrowser

from urllib import request
from urllib.parse import parse_qsl
from urllib.parse import urlparse
import oauth2 as oauth


class AuthScreen:
    consumerKey = 'DtnKgLrTlfWnVIkyirOB'
    consumerSecret = 'eUydCQVQhzKYDnCBdEQOTLfVWedyIlRa'

    request_token_url = 'https://api.discogs.com/oauth/request_token'
    authorize_url = 'https://www.discogs.com/oauth/authorize'
    access_token_url = 'https://api.discogs.com/oauth/access_token'

    userAgent = 'RecordCollectionDisplay/0.1 +https://github.com/thelemon2020/RecordCollectionDisplay'
    def __init__(self):
        self.consumer = oauth.Consumer(self.consumerKey, self.consumerSecret)

    def showWindow(self):
        self.window = tk.Tk()
        greeting = tk.Label(text="Welcome to Your Record Collection")
        greeting.pack()
        self.authAppStep1()
        url = self.authorize_url+ '?oauth_token=' + self.request_token["oauth_token"]
        urlMessage = tk.Label(text = 'Please browse to the following URL to authorize app:')
        urlMessage.pack()
        urlToVisit = tk.Label(text = url, fg="blue", cursor="hand2")
        urlToVisit.pack()
        urlToVisit.bind("<Button-1>", lambda e: self.callback(url))
        self.verificationCode = tk.Entry()
        self.verificationCode.pack()
        submitButton = tk.Button(text="Submit")
        submitButton.bind("<Button-1>", self.handle_click)
        submitButton.pack()
        self.window.mainloop()

    def callback(self,url):
        webbrowser.open_new(url)

    def handle_click(self,event):
        code = self.verificationCode.get()
        self.authAppStep2(code)
        self.window.destroy()

    def authAppStep1(self):
        client = oauth.Client(self.consumer)
        resp, content = client.request(self.request_token_url, 'POST', headers={'User-Agent': self.userAgent})
        if resp['status'] != '200':
            sys.exit('Invalid response {0}.'.format(resp['status']))

        self.request_token = dict(parse_qsl(content.decode('utf-8')))

    def authAppStep2(self, oauth_verifier):
        token = oauth.Token(self.request_token['oauth_token'], self.request_token['oauth_token_secret'])
        token.set_verifier(oauth_verifier)
        client = oauth.Client(self.consumer, token)

        resp, content = client.request(self.access_token_url, 'POST', headers={'User-Agent': self.userAgent})

        access_token = dict(parse_qsl(content.decode('utf-8')))

        token = oauth.Token(key=access_token['oauth_token'],
            secret=access_token['oauth_token_secret'])
        file = open("token.txt","w")
        file.write(token.key + "," + token.secret)
        file.close()