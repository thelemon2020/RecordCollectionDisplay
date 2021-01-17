import tkinter as tk
import json
import sys
import RecordCollectionDisplay
import oauth2 as oauth

class MainWindow:
    def __init__(self, client):
        self.oauthClient = client

    def start():

        window = tk.Tk()
