import tkinter as tk
import json
import sys
import RecordCollectionDisplay
import oauth2 as oauth
import Entry
from PIL import Image, ImageTk
import requests

userAgent = 'RecordCollectionDisplay/0.1 +https://github.com/thelemon2020/RecordCollectionDisplay'

class MainWindow(tk.Frame):
    def __init__(self, parent,client, userName):        
        self.oauthClient = client
        self.userName = userName
        self.collectionEntries = self.getEntries(userName, '0', 'artist')
        self.folders = self.getFolders(userName)
        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")
        self.frame = tk.Frame(self.canvas, background="#ffffff")
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw",
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)
        collectionItems = self.collectionEntries.items()
        for key, value in collectionItems:
            artistLabel = tk.Label(master = self.frame, text = value.artist).grid(row=key, column =0)
            titleLabel = tk.Label(master = self.frame, text = value.title).grid(row=key, column =1)
            imageLabel = tk.Label(master = self.frame, width= 50, height = 50)
            imageLabel.grid(row=key, column = 2)
            im = Image.open(requests.get(value.imageURL, stream=True).raw)
            im = im.resize((25,25), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(im) 
            imageLabel.image = img
            imageLabel.configure(image=img)

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

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

