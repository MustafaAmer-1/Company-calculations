from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import sqlite3

## window with full scall ##

root = Tk()
root.state('zoomed')
root.bind("<F12>", lambda event: root.attributes("-fullscreen", True))
root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))

## connect to the data base ##

class dataBase:
    def __init__(self, fileName):
        try:
            self.conn = sqlite3.connect(fileName)
            self.cur = self.conn.cursor()
        except:
            messagebox.showerror("DataBase corrupted", "Open new DataBase file")
            root.filename = filedialog.askopenfile(initialdir="/", title="Select DataBase File", filetypes=(("db files", "*.db")))
            self.__init__(root.fileName)

dataBase = dataBase("items.db")
conn = dataBase.conn
cur = dataBase.cur


root.mainloop()