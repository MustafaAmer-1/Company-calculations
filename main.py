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

## Create treeView Frame ##
tree_frame = Frame(root)
tree_frame.pack(pady=20)

## Create Treeview ScrollBar ##
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)

## Create items treeview ##
items_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)

## Pack the treeview to the window ##
items_tree.pack(fill=X)

## Configure ScrollBar ##
tree_scroll.config(command=items_tree.yview)

## define the columns ##
items_tree['columns'] = ("ID", "Name", "Price")

## Format the columns ##
items_tree.column("#0", width=0, stretch=NO) # Phantom column
items_tree.column("ID", anchor=W, width=400)
items_tree.column("Name", anchor=W, width=1200)
items_tree.column("Price", anchor=W, width=800)

## Create Headings ##
items_tree.heading("#0", text="", anchor=W)
items_tree.heading("ID", text="ID", anchor=W)
items_tree.heading("Name", text="Name", anchor=W)
items_tree.heading("Price", text="Price", anchor=W)

## style the treeView ##
style = ttk.Style(root)
style.theme_use("clam")
style.configure("Treeview",
             rowheight=70)

items_tree.configure(style="Treeview")

## Create striped row with tags ##
items_tree.tag_configure('evenRow', background='lightblue')
items_tree.tag_configure('oddRow', background='white')

## TreeView Data ##
cur.execute("SELECT * FROM items")
for id, name, price in cur.fetchall():
    if id % 2 == 0:
        items_tree.insert(parent='', index='end', iid=id, values=(id, name, price), tags=('evenRow', ))
    else:
        items_tree.insert(parent='', index='end', iid=id, values=(id, name, price), tags=('oddRow', ))

root.mainloop()