import RecordCollectionDisplay
import tkinter as tk

class LogScreen:
    def __init__(self):
        self.window = tk.Tk()
        prompt = tk.Label(text='Enter your Discogs username')
        prompt.pack()
        self.userNamePrompt = tk.Entry()
        self.userNamePrompt.pack()
        submitButton = tk.Button(text='Submit')
        submitButton.bind('<Button-1>', self.submitEvent)
        submitButton.pack()
    
    def submitEvent(self, event):
        userName = self.userNamePrompt.get()
        file = open("user.txt","w")
        file.write(userName)
        file.close()
        self.window.destroy()

    def ShowWindow(self):
        self.window.mainloop()
