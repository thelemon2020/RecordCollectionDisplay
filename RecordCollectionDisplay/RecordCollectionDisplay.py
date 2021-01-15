import tkinter as tk

welcomeWindow = tk.Tk()

def getList():
    res = requests.get("https://api.discogs.com/users/thelemon.chris/collection/folders/0/releases?sort=artist&page=")