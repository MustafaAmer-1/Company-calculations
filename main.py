from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
import sqlite3

## window with full scall ##

root = Tk()
root.title("Company calculations with Tkinter")
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

## create the items table ##

cur.execute('''CREATE TABLE IF NOT EXISTS "items" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT,
	"price"	REAL,
	PRIMARY KEY("id" AUTOINCREMENT)
);''')

## set items treeview ##
items_tree = ttk.Treeview(root)

## define the columns ##
items_tree['columns'] = ("ID", "Name", "Price")

## Format the columns ##
items_tree.column("#0", width=0, minwidth=0) # Phantom column
items_tree.column("ID", anchor=W, width=80)
items_tree.column("Name", anchor=W, width=120)
items_tree.column("Price", anchor=E, width=80)

## Create Headings ##
items_tree.heading("#0", text="", anchor=W)
items_tree.heading("ID", text="Item ID", anchor=W)
items_tree.heading("Name", text="Item Name", anchor=W)
items_tree.heading("Price", text="Item Price", anchor=E)

## TreeView Data ##
items_tree.insert(parent='', index='end', iid=0, text="Parent", values=("First", 1, "Apple"))

## Pack the treeview to the window ##
items_tree.pack()

root.mainloop()