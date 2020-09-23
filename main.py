from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
import sqlite3

class my_tree(ttk.Treeview):
    tree_frame = None
    def __init__(self, master, **kwargs):
        self.tree_frame = Frame(master)
        self.tree_frame.pack(side=TOP, fill = BOTH)

        self.tree_scroll = Scrollbar(self.tree_frame)
        self.tree_scroll.pack(side=RIGHT, fill=Y)

        super(my_tree, self).__init__(self.tree_frame,
                    yscrollcommand=self.tree_scroll.set , **kwargs)

        self.tree_scroll.config(command=self.yview)

    def Make_heading_columns(self, *args):
        self.column("#0", width=0, stretch=NO)
        self.heading("#0", text="", anchor=W)

        for ar in args:
            name = ar.split()[0]
            width=int(ar.split()[1])
            self.column(name, width=width, anchor=W)
            self.heading(name, text=name, anchor=W)

## window with full scall ##
root = Tk()
root.title("Company calculations with Tkinter")
root.state('zoomed')
root.bind("<F12>", lambda event: root.attributes("-fullscreen", True))
root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))

## Calculate the size of the screen ##
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

## Create Main Menu ##
main_menu = Menu(root)
root.config(menu=main_menu)

## Create items menu ##
item_menu = Menu(main_menu, tearoff=0)
main_menu.add_cascade(menu=item_menu, label="Items")

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

## Create items treeview ##
items_tree = my_tree(root)

## Create selected items treeview ##
selected_tree = my_tree(root)

## Pack the items treeview to the window ##
items_tree.pack(fill=X)

## Pack the selected items treeview to the window ##
selected_tree.pack(fill=X)

## define the columns ##
items_tree['columns'] = ("ID", "Name", "Price")
selected_tree['columns'] = ("Name", "Price", "Amount", "Total")

## Create Column and Headings ##
items_tree.Make_heading_columns("ID 10", "Name 1200", "Price 80")
selected_tree.Make_heading_columns("Name 120", "Price 40", "Amount 80", "Total 80")

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

## items TreeView Data ##
cur.execute("SELECT * FROM items")
for id, name, price in cur.fetchall():
    price = ('%f' % price).rstrip('0').rstrip('.')
    if id % 2 == 0:
        items_tree.insert(parent='', index='end', iid=int(id), values=(id, name, price), tags=('evenRow', ))
    else:
        items_tree.insert(parent='', index='end', iid=int(id), values=(id, name, price), tags=('oddRow', ))

def open_add_item_window():
    global add_item_window
    add_item_window = Toplevel(root)
    
    Label(add_item_window, text="Item Name", padx=10, pady=10).grid(row=0, column=0, sticky=E)
    
    name_entry = Entry(add_item_window, borderwidth=5)
    name_entry.grid(row=0, column=1)
    
    Label(add_item_window, text="Item Price", padx=10, pady=10).grid(row=1, column=0, sticky=E)
    
    price_entry = Entry(add_item_window, borderwidth=5)
    price_entry.grid(row=1, column=1)

    add_button = Button(add_item_window, text="ADD", padx=10, pady=10
                            , borderwidth=5, bg="#70E852", command=lambda : add_item(name_entry.get(), price_entry.get()))
    add_button.grid(row=2, columnspan=2, sticky="nsew")

    name_entry.focus_set()

    add_item_window.bind("<Return>", lambda event: add_button.invoke())
    return

## Add item to the DataBase and items TreeView ##
def add_item(name, price):
    cur.execute("INSERT INTO items (name, price) VALUES (?, ?)", (name, price))
    last_id = cur.lastrowid
    if last_id % 2 == 0:
        items_tree.insert(parent='', index='end', iid=int(last_id), values=(last_id, name, price), tags=('evenRow', ))
    else:
        items_tree.insert(parent='', index='end', iid=int(last_id), values=(last_id, name, price), tags=('oddRow', ))
    conn.commit()
    add_item_window.destroy()
    return

## Create add item command to Items Menu ##
item_menu.add_command(label="Add Item...", command=open_add_item_window)

## add selected item to the selected treeView ##
def add_selected_item(event):
    item_num = items_tree.focus()
    values = items_tree.item(item_num, "values")
    try:
        selected_tree.insert(parent='', index='end', iid=int(values[0]), values=(values[1], values[2], 1, values[2]), tags=('selectedRow', ))
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
        amount_view = Toplevel(selected_tree.tree_frame)
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

## Add Quit command to items menu ##
def end_program():
    answer = messagebox.askyesno("Quit Program", "Do you want to end the program?")
    if answer:
        root.quit()

## Handel root window close and create Messagebox ##
#root.protocol("WM_DELETE_WINDOW", end_program)
## fast Quit the program with Ctrl-Q without asking ##
root.bind("<Control-Key-q>", lambda event: root.quit())

## print the bill ##
def print_bill(window):
    window.destroy()

## Open pre prented window with final totals ##
def open_prePrinted_window():
    prePrinted_window = Toplevel(root)
    prePrinted_window.geometry("600x600")

    ## Create prePrinted treeView ##
    prePrinted_treeView = my_tree(prePrinted_window)
    prePrinted_treeView['columns'] = ("Name", "Price", "Amount", "Total")
    prePrinted_treeView.Make_heading_columns("Name 120", "Price 80", "Amount 80", "Total 80")
    prePrinted_treeView.pack(fill=X)

    prePrinted_treeView.tag_configure('prePrinted', background='#FE9E76')

    ## Add Date From seleted treeView ##
    total = 0
    for child in selected_tree.get_children():
        values = selected_tree.item(child, 'values')
        prePrinted_treeView.insert(parent='', index='end', iid=child, values=values, tags=('prePrinted', ))
        total += float(values[-1])
    total = ('%f' % total).rstrip('0').rstrip('.')
    
    total_frame = Frame(prePrinted_window, bg="#B9789F")
    total_frame.pack(fill=BOTH, expand=True)
    Label(total_frame, text=" Total: ", font=("Helvetica", 13), bg="#B9789F").pack(side=LEFT)
    #.place(x=60, y=35, anchor="center")
    Label(total_frame, text=total, font=("Helvetica", 13), bg="#B9789F").pack(side=LEFT)
    #.place(x=120, y=35, anchor="center")

    Label(total_frame, text="  ", font=("Helvetica", 13), bg="#B9789F").pack(side=RIGHT)
    
    final_total_entry = Entry(total_frame, font=("Helvetica", 13), width=10, borderwidth=2)
    final_total_entry.insert(0, total)
    final_total_entry.pack(side=RIGHT)
    final_total_entry.focus_set()
    final_total_entry.selection_range(0, END)

    Label(total_frame, text="After Discount: ", font=("Helvetica", 13), bg="#B9789F").pack(side=RIGHT)

    button_frame = Frame(prePrinted_window, bg="#B9789F")
    button_frame.pack(fill=BOTH, expand=True)

    submit_button = Button(button_frame, text="SUBMIT!", command=lambda: print_bill(prePrinted_window), padx=50)
    submit_button.pack()

    prePrinted_window.bind("<Return>", lambda event: submit_button.invoke())


## Create print bill command to Items menue ##
item_menu.add_command(label="Print Bill", command=open_prePrinted_window)

## Bind Ctrl-P to open pre-print window ##
root.bind("<Control-Key-p>", lambda event: open_prePrinted_window())

## Create Quit command to items menu ##
item_menu.add_separator()
item_menu.add_command(label="Quit", command=end_program)


root.mainloop()