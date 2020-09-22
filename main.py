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

## Calculate the size of the screen ##
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
#print(screen_width, screen_height)

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

## Create items treeView Frame ##
tree_frame = Frame(root, bg="blue")
tree_frame.pack(side=TOP, expand = True, fill = BOTH)

## Create selected items TreeView Frame ##
selected_frame = Frame(root, bg="red")
selected_frame.pack(side=BOTTOM, expand = True, fill = BOTH)

## Create items Treeview ScrollBar ##
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)

## Create selected items Treeview ScrollBar ##
selected_scroll = Scrollbar(selected_frame)
selected_scroll.pack(side=RIGHT, fill=Y)

## Create items treeview ##
items_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)

## Create selected items treeview ##
selected_tree = ttk.Treeview(selected_frame, yscrollcommand=selected_scroll.set)

## Pack the items treeview to the window ##
items_tree.pack(fill=X)

## Pack the selected items treeview to the window ##
selected_tree.pack(fill=X)

## Configure ScrollBar ##
tree_scroll.config(command=items_tree.yview)
selected_scroll.config(command=selected_tree.yview)

## define the columns ##
items_tree['columns'] = ("ID", "Name", "Price")
selected_tree['columns'] = ("Name", "Price", "Amount", "Total")

## Format the columns for items ##
items_tree.column("#0", width=0, stretch=NO) # Phantom column
items_tree.column("ID", anchor=W, width=10)
items_tree.column("Name", anchor=W, width=1200)
items_tree.column("Price", anchor=W, width=80)

## Format the columns for selected items##
selected_tree.column("#0", width=0, stretch=NO) # Phantom column
selected_tree.column("Name", anchor=W, width=120)
selected_tree.column("Price", anchor=W, width=40)
selected_tree.column("Amount", anchor=W, width=80)
selected_tree.column("Total", anchor=W, width=80)

## Create Headings for items tree view ##
items_tree.heading("#0", text="", anchor=W)
items_tree.heading("ID", text="ID", anchor=W)
items_tree.heading("Name", text="Name", anchor=W)
items_tree.heading("Price", text="Price", anchor=W)

## Create Headings for selected tree view ##
selected_tree.heading("#0", text="", anchor=W)
selected_tree.heading("Name", text="Name", anchor=W)
selected_tree.heading("Price", text="Price", anchor=W)
selected_tree.heading("Amount", text="Amount", anchor=W)
selected_tree.heading("Total", text="Total", anchor=W)

## style the treeView ##
style = ttk.Style(root)
style.theme_use("clam")
style.configure("Treeview",
             rowheight=50)

items_tree.configure(style="Treeview")

selected_tree.configure(style="Treeview")

## Create striped row with tags items##
items_tree.tag_configure('evenRow', background='lightblue')
items_tree.tag_configure('oddRow', background='white')

## Create striped row with tags selected##
selected_tree.tag_configure('selectedRow', background='#FFF851')

## TreeView Data ##
cur.execute("SELECT * FROM items")
for id, name, price in cur.fetchall():
    price = ('%f' % price).rstrip('0').rstrip('.')
    if id % 2 == 0:
        items_tree.insert(parent='', index='end', iid=int(id), values=(id, name, price), tags=('evenRow', ))
    else:
        items_tree.insert(parent='', index='end', iid=int(id), values=(id, name, price), tags=('oddRow', ))

## add selected item to the selected treeView ##
def add_selected_item(event):
    item_num = items_tree.focus()
    values = items_tree.item(item_num, "values")
    try:
        selected_tree.insert(parent='', index='end', iid=int(values[0]), values=(values[1], values[2]), tags=('selectedRow', ))
    except:
        pass

## edit the amount of selected item ##
def edit_the_amount(event):

    ## close the view and update the selected item with new amount ##
    def close_view(event):
        try:
            amount = int(e.get())
            total = amount*selected_price
            total = ('%f' % total).rstrip('0').rstrip('.')
            selected_tree.item(selected_num, values=(selected_name, selected_price, amount, total))
            amount_view.destroy()
        except:
            messagebox.showwarning("Non-Falid Amount", "Enter Integer Number for the Amount!")
            e.focus_set()
    
    ## open amount view and bind enter event to close the view ##
    def open_amount_view(num ,name, price):
        global selected_name
        selected_name = name
        global selected_price
        selected_price = price
        global selected_num
        selected_num = num

        global amount_view
        amount_view = Toplevel(selected_frame)
        amount_view.title("Amount of " + selected_name)
        Label(amount_view, text="Amount of " + selected_name).grid(padx=10, pady=20, row=0, column=0)
        global e
        e = Entry(amount_view)
        e.focus_set()
        e.grid(row=0, column=1, pady=20, padx=10)
        amount_view.bind('<Return>', close_view)

    selected_num = selected_tree.focus()
    current_values = selected_tree.item(selected_num, 'values')
    price = float(current_values[1])
    name = current_values[0]
    open_amount_view(selected_num, name, price)

## delete the selected item from the treeView ##
def delete_selected_item(event):
    try:
        selected_tree.delete(selected_tree.focus())
        next_selection = selected_tree.get_children()[0]
        selected_tree.focus(next_selection)
        selected_tree.selection_set(next_selection)
    except:
        pass

## Bind Double click event to items tree view to insert items to selected ##
items_tree.bind("<Double-1>", add_selected_item)

## Bind Double click event to selected items to edit the Amount ##
selected_tree.bind("<Double-1>", edit_the_amount)

## Bind enter to edit the selected item amount ##
try:
    selected_tree.bind("<Return>", edit_the_amount)
except:
    pass

## Bind delete key event to delete the selected item ##
try:
    selected_tree.bind("<Delete>", delete_selected_item)
except:
    pass

root.mainloop()