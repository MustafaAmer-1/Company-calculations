from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
import sqlite3


class my_tree_view():
    def __init__(self, root, *args, **kwargs):
        ## Create treeView Frame ##
        self.my_tree_frame = Frame(root)
        self.my_tree_frame.pack(expand = True, fill = BOTH)

        ## Create TreeView ScrollBar ##
        self.my_scroll = Scrollbar(self.my_tree_frame)
        self.my_scroll.pack(side=RIGHT, fill=Y)

        ## Create Treeview ##
        self.my_tree = ttk.Treeview(self.my_tree_frame, yscrollcommand=self.my_scroll.set)

        ## pack treeView to the window ##
        self.my_tree.pack(fill=X)

        ## Configure ScrollBar ##
        self.my_scroll.config(command=self.my_tree.yview)

        ## define the columns ##
        self.my_tree['columns'] = args

        ## Format the columns and Headings for the tree ##
        self.my_tree.column("#0", width=0, stretch=NO) # Phantom column
        self.my_tree.heading("#0", text="", anchor=W)  # Phanto, heading
        for column in args:
            self.my_tree.column(column, anchor=W, width=kwargs.get(column+"Width", 100))
            self.my_tree.heading(column, text=column, anchor=W)

        ## style the treeView ##
        self.style = ttk.Style(root)
        self.style.theme_use("clam")
        self.style.configure("Treeview",
                        rowheight=50)

        self.my_tree.configure(style="Treeview")

    def insert(self, **kwargs):
        self.my_tree.insert(parent='', index='end', iid=kwargs.get("iid"), values=kwargs.get("values"), tags=kwargs.get("tags"))

    def tag_configure(self, name,**kwargs):
        self.my_tree.tag_configure(name, background=kwargs.get("background", "white"))


root = Tk()
root.title("Company calculations with Tkinter")
root.state('zoomed')
root.bind("<F12>", lambda event: root.attributes("-fullscreen", True))
root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))   

items_tree = my_tree_view(root, "ID", "Name", "Price", IDWidth=10, NameWidth=1200, PriceWidth=80)
items_tree.tag_configure('evenRow', background='lightblue')
items_tree.tag_configure('oddRow', background='white')

