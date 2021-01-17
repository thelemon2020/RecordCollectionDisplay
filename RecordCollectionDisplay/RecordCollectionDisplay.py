import authScreen
import LogScreen
import oauth2 as oauth
import os.path
import MainWindow

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
   resp, content = client.request('https://api.discogs.com/users/' + userName + '/collection/folders/0/releases?sort=artist', headers={'User-Agent': userAgent})
   print(content)

if __name__ == "__main__":
    main()