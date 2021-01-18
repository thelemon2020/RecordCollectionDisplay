import tkinter as tk
import json
import sys
import RecordCollectionDisplay
import oauth2 as oauth
import Entry
from PIL import Image, ImageTk
import requests

userAgent = 'RecordCollectionDisplay/0.1 +https://github.com/thelemon2020/RecordCollectionDisplay'

class MainWindow:
    def __init__(self, client, userName):
        self.oauthClient = client
        self.userName = userName
        self.collectionEntries = self.getEntries(userName, '0', 'artist')
        self.folders = self.getFolders(userName)

    def getFolders(self, userName):
        resp, content = self.oauthClient.request('https://api.discogs.com/users/' + userName + '/collection/folders',  headers = {'User-Agent': userAgent})
        folders = json.loads(content.decode('utf-8'))
        folderDict = {}
        for folder in folders['folders']:
            folderID = folder['id']
            folderName = folder['name']
            folderDict[folderName] = folderID
        return folderDict

    def getEntries(self, userName, folder, sort):
        resp, content = self.oauthClient.request('https://api.discogs.com/users/' + userName + '/collection/folders/' + folder +'/releases?sort=' + sort, headers = {'User-Agent': userAgent})
        releases =json.loads(content.decode('utf-8'))
        releaseDict = {}
        i = 1
        for release in releases['releases']:
            title = release['basic_information']['title']
            artist = release['basic_information']['artists'][0]['name']
            imageURL = release['basic_information']['thumb']
            newEntry = Entry.Entry(artist, title, imageURL, '0')
            releaseDict[i] = newEntry
            i = i + 1
        return releaseDict

    def start(self):
        window = tk.Tk()
        frame = tk.Frame(master=window)
        frame.grid(row=len(self.collectionEntries), column = 3)
        frame.pack()
        collectionItems = self.collectionEntries.items()
        scrollbar = tk.Scrollbar(master = window)
        scrollbar.pack(side = tk.RIGHT, fill= tk.Y)
        for key, value in collectionItems:
            artistLabel = tk.Label(master = frame, text = value.artist).grid(row=key, column =0)
            titleLabel = tk.Label(master = frame, text = value.title).grid(row=key, column =1)
            canvas = tk.Canvas(master = frame, width= 50, height = 50)
            canvas.grid(row = key, column = 2)
            im = Image.open(requests.get(value.imageURL, stream=True).raw)
            im = im.resize((25,25), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(im) 
            canvas.create_image(0,0,image=img)
        window.mainloop()

