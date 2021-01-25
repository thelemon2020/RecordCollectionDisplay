import authScreen
import LogScreen
import oauth2 as oauth
import os.path
import MainWindow
import tkinter as tk

tokenFile = 'token.txt'
userFile = 'user.txt'
consumerKey = 'DtnKgLrTlfWnVIkyirOB'
consumerSecret = 'eUydCQVQhzKYDnCBdEQOTLfVWedyIlRa'
userAgent = 'RecordCollectionDisplay/0.1 +https://github.com/thelemon2020/RecordCollectionDisplay'

def main():
   
   if (os.path.isfile(tokenFile) == False):
       auth = authScreen.AuthScreen()
       auth.showWindow()
   if (os.path.isfile(userFile) == False):
       log = LogScreen.LogScreen()
       log.ShowWindow()
   file = open(tokenFile, 'r')
   tokens = file.read().split(',')
   file.close()
   file = open(userFile, 'r')
   userName = file.read()
   authTokens = oauth.Token(key = tokens[0], secret = tokens[1])
   consumer = oauth.Consumer(consumerKey, consumerSecret)
   client = oauth.Client(consumer, authTokens)
   root = tk.Tk()
   RecordScreen = MainWindow.MainWindow(root, client, userName)
   RecordScreen.pack(side="top", fill="both", expand=True)
   root.mainloop()
   

if __name__ == "__main__":
    main()