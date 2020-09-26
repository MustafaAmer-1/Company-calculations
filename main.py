from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
import sqlite3
from docxtpl import DocxTemplate
import datetime  
import os, sys, win32print, win32api 
from shutil import copy2, move

## exit from the program ##
def endTheProgram():
    messagebox.showerror("النسخة انتهت", "انتهت عدد مرات استخدام النسخة المجانية \n من فضلت قم بشراء البرنامج")
    quit()

## connect to counts data base ##
countsConn = sqlite3.connect("Files/items2.db")
countsCur = countsConn.cursor()

## get the counts from the data base ##
try:
    countsCur.execute("SELECT countOfLogin FROM counts")
    if countsCur.fetchone()[0] > 2:
        endTheProgram()
    else:
        countsCur.execute("UPDATE counts SET countOfLogin = countOfLogin + 1")
        countsConn.commit()
        pass

except:
    endTheProgram()

class dataBase:
    def __init__(self, fileName):
        try:
            self.conn = sqlite3.connect("Files/" + fileName)
            self.cur = self.conn.cursor()
        except:
            messagebox.showerror("DataBase corrupted", "Open new DataBase file")
            root.filename = filedialog.askopenfile(initialdir="/", title="Select DataBase File", filetypes=(("db files", "*.db")))
            self.__init__(root.fileName)

## connect to items data base ##
dataBase = dataBase("itemsWithCode.db")
conn = dataBase.conn
cur = dataBase.cur

## Make copy of the data base ##
#copy2("items.db", "DB_Copy/items_copy.db")

## create the items table ##
cur.execute('''CREATE TABLE IF NOT EXISTS "items" (
    "id"	INTEGER NOT NULL UNIQUE,
    "name"	TEXT,
    "price"	REAL,
    "code" INTEGER NOT NULL,
    PRIMARY KEY("id" AUTOINCREMENT)
);''')

## Create office names table ##
cur.execute('''CREATE TABLE IF NOT EXISTS "office_names"(
    "id"	INTEGER NOT NULL UNIQUE,
    "name" TEXT,
    PRIMARY KEY("id" AUTOINCREMENT)
);''')

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
        self.heading("#0", text="", anchor=E)

        for ar in args:
            name = ar.split()[0]
            width=int(ar.split()[1])
            self.column(name, width=width, anchor=E)
            self.heading(name, text=name, anchor=E)

## window with full scall ##
root = Tk()
root.title("Company calculations with Tkinter")
root.state('zoomed')
root.bind("<F12>", lambda event: root.attributes("-fullscreen", True))
root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))

## Calculate the size of the screen ##
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

## Create SearchBar ##
search_entry = Entry(root, borderwidth=2, width=50)
search_entry.pack(side=TOP)
search_entry.insert(0, "Search")
search_entry.selection_range(0, END)
search_entry.focus_set()
search_entry.bind("<Return>", lambda event: select_searched_item(search_entry))

## Create Main Menu ##
main_menu = Menu(root)
root.config(menu=main_menu)

## Create items menu ##
item_menu = Menu(main_menu, tearoff=0)
main_menu.add_cascade(menu=item_menu, label="الموديلات")

## Create Bill menu ##
bill_menu = Menu(main_menu, tearoff=0)
main_menu.add_cascade(menu=bill_menu, label="الفاتورة")

## Create items treeview ##
items_tree = my_tree(root)

## Create selected items treeview ##
selected_tree = my_tree(root)

## Pack the items treeview to the window ##
items_tree.pack(fill=X)

## Pack the selected items treeview to the window ##
selected_tree.pack(fill=X)

## define the columns ##
items_tree['columns'] = ("السعر",
                             "الاسم",
                              "الكود")

selected_tree['columns'] = ("الاجمالي",
                                 "الكمية",
                                  "السعر",
                                   "الاسم",
                                   "الكود")

## Create Column and Headings ##
items_tree.Make_heading_columns("السعر 10", "الاسم 600", "الكود 80")
selected_tree.Make_heading_columns("الاجمالي 80", "الكمية 40", "السعر 80", "الاسم 80", "الكود 80")

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
cur.execute("SELECT name, price, code, id FROM items")
for name, price, code, id in cur.fetchall():
    price = ('%f' % price).rstrip('0').rstrip('.')
    if id % 2 == 0:
        items_tree.insert(parent='', index='end', iid=int(id), values=(price, name, code), tags=('evenRow', ))
    else:
        items_tree.insert(parent='', index='end', iid=int(id), values=(price, name, code), tags=('oddRow', ))

def open_add_item_window():
    global add_item_window
    add_item_window = Toplevel(root)
    
    Label(add_item_window, text="كود الموديل", padx=10, pady=10).grid(row=0, column=0, sticky=E)

    code_entry = Entry(add_item_window, borderwidth=5)
    code_entry.grid(row=0, column=1, padx=10)

    Label(add_item_window, text="اسم الموديل", padx=10, pady=10).grid(row=1, column=0, sticky=E)
    
    name_entry = Entry(add_item_window, borderwidth=5)
    name_entry.grid(row=1, column=1, padx=10)
    
    Label(add_item_window, text="سعر الموديل", padx=10, pady=10).grid(row=2, column=0, sticky=E)
    
    price_entry = Entry(add_item_window, borderwidth=5)
    price_entry.grid(row=2, column=1, pady=10)

    add_button = Button(add_item_window, text="ADD", padx=10, pady=10
                            , borderwidth=5, bg="#70E852", command=lambda : add_item(name_entry, price_entry, code_entry))
    add_button.grid(row=3, columnspan=2, sticky="nsew")

    code_entry.focus_set()

    add_item_window.bind("<Return>", lambda event: add_button.invoke())
    return

## Add item to the DataBase and items TreeView ##
def add_item(name_entry, price_entry, code_entry):
    name = name_entry.get()
    price = price_entry.get()
    code = code_entry.get()
    try:
        price = float(price)
        price = ('%f' % price).rstrip('0').rstrip('.')
    except:
        messagebox.showerror("Non Falid Price", "Please Enter Real Number in the price")
        price_entry.focus_set()
        return

    cur.execute("INSERT INTO items (name, price, code) VALUES (?, ?, ?)", (name, price, code))
    last_id = cur.lastrowid
    if last_id % 2 == 0:
        items_tree.insert(parent='', index='end', iid=int(last_id), values=(price, name, code), tags=('evenRow', ))
    else:
        items_tree.insert(parent='', index='end', iid=int(last_id), values=(price, name, code), tags=('oddRow', ))
    conn.commit()
    ## Delete the entries ##
    name_entry.delete(0, END)
    price_entry.delete(0, END)
    code_entry.delete(0,END)
    code_entry.focus_set()

    #add_item_window.destroy()
    return

## Create add item command to Items Menu ##
item_menu.add_command(label="اضافة عنصر .. (Ctrl-N)", command=open_add_item_window)

## add selected item to the selected treeView ##
def add_selected_item(event):
    item_num = items_tree.focus()
    values = items_tree.item(item_num, "values")
    try:
        selected_tree.insert(parent='', index='end', iid=item_num, values=(values[0], 1, values[0], values[1], values[2]), tags=('selectedRow', ))
    except:
        pass

## edit the amount of selected item ##
def edit_the_amount(event):

    ## close the view and update the selected item with new amount ##
    def close_view(num, name, price, code, e):
        try:
            amount = int(e.get())
            total = amount*price
            total = ('%f' % total).rstrip('0').rstrip('.')
            price = ('%f' % price).rstrip('0').rstrip('.')
            selected_tree.item(num, values=(total, amount, price, name, code))
            amount_view.destroy()
        except:
            messagebox.showwarning("Non-Falid Amount", "Enter Integer Number for the Amount!")
            e.focus_set()
    
    ## open amount view and bind enter event to close the view ##
    def open_amount_view(num ,name, price, code):
        global amount_view
        amount_view = Toplevel(selected_tree.tree_frame)
        amount_view.title("الكمية")
        Label(amount_view, text="الكمية من " + name).grid(padx=10, pady=20, row=0, column=1)
        e = Entry(amount_view)
        e.focus_set()
        e.grid(row=0, column=0, pady=20, padx=10)
        amount_view.bind('<Return>',lambda event: close_view(num, name, price, code, e))

    selected_num = selected_tree.focus()
    current_values = selected_tree.item(selected_num, 'values')
    price = float(current_values[2])
    name = current_values[3]
    code = current_values[4]
    open_amount_view(selected_num, name, price, code)

## delete the selected item from the treeView ##
def delete_selected_item(event):
    try:
        selected_tree.delete(selected_tree.focus())
        ## set the selection to the first item in the tree ##
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

## Create real print file function ##
def print_file(file_to_print):
    countsCur.execute("SELECT countOfPrint FROM counts")
    if countsCur.fetchone()[0] > 2:
        endTheProgram()
    else:
        countsCur.execute("UPDATE counts SET countOfPrint = countOfPrint + 1 ")
        if file_to_print:
            win32api.ShellExecute(0, "print", file_to_print, None, ".", 0)
            win32api.ShellExecute(0, "print", file_to_print, None, ".", 0)
            countsConn.commit()

## generate the bill docx ##
def generate_docx(window, disEntry, office_compo):
    ## Add entered office name to data base ##
    if office_compo.current() == -1:
        cur.execute("INSERT INTO office_names (name) VALUES (?)", (office_compo.get(),))
        conn.commit()

    ## Calculate Current Time and Date ##
    current_time = str(datetime.datetime.now())
    current_time = current_time[:current_time.index(".")]
    file_name = current_time.replace(":", "-")

    ## open Bill Template ##
    try:
        tpl = DocxTemplate('Files/FatoraWithCode.tmp')

        ## Create tmpl Contex ##
        context = {}

        context["total"] = disEntry.get()
        context["tbl_headers"] = [
            {
                "office":office_compo.get(),
                "date": str(datetime.datetime.now().date()) 
                }
        ]
        context["tbl_contents"] = []

        total_quantity = 0

        childeren = selected_tree.get_children()
        for child in childeren:
            values = selected_tree.item(child, 'values')
            context["tbl_contents"].append({
                'test' : values[4],
                'label' : values[3],
                "cols": values[:3]
            })

            total_quantity += int(values[1])

        context['quantity'] = total_quantity

        ## Render the Contex ##
        tpl.render(context)
        tpl.save(file_name + ".docx")

    ## Handle Any Error During opening and rendering and saving file ##
    except:
        messagebox.showerror("Bill Template", "The program failed to open Bill template")
        
    ## print the docx file ##
    print_file(file_name + ".docx")

    window.destroy()


## Open pre prented window with final totals ##
def open_prePrinted_window():
    bottom_color = "#FFF851"

    prePrinted_window = Toplevel(root, bg=bottom_color)
    prePrinted_window.geometry("600x700")

    ## Create prePrinted treeView ##
    prePrinted_treeView = my_tree(prePrinted_window)
    prePrinted_treeView['columns'] = ("الاجمالي",
                                 "الكمية",
                                  "السعر",
                                   "الاسم",
                                   "الكود")
    prePrinted_treeView.Make_heading_columns("الاجمالي 80", "الكمية 40", "السعر 80", "الاسم 80", "الكود 80")
    prePrinted_treeView.pack(fill=X)

    prePrinted_treeView.tag_configure('prePrinted', background='#FE9E76')

    ## Add Date From seleted treeView ##
    total = 0
    childeren = selected_tree.get_children()
    for child in childeren:
        values = selected_tree.item(child, 'values')
        prePrinted_treeView.insert(parent='', index='end', iid=child, values=values, tags=('prePrinted', ))
        total += float(values[0])

    total = ('%f' % total).rstrip('0').rstrip('.')

    total_frame = Frame(prePrinted_window, bg=bottom_color)
    total_frame.pack(fill=BOTH, expand=True)
    Label(total_frame, text="   الاجمالي   ", font=("Helvetica", 13), bg=bottom_color).pack(side=RIGHT)
    Label(total_frame, text=total, font=("Helvetica", 13), bg=bottom_color, padx=10).pack(side=RIGHT)

    Label(total_frame, text="  ", font=("Helvetica", 13), bg=bottom_color).pack(side=LEFT)

    final_total_entry = Entry(total_frame, font=("Helvetica", 13), width=10, borderwidth=2)
    final_total_entry.insert(0, total)
    final_total_entry.pack(side=LEFT)
    final_total_entry.focus_set()
    final_total_entry.selection_range(0, END)

    Label(total_frame, text="    بعد الخصم", font=("Helvetica", 13), bg=bottom_color).pack(side=LEFT)

    ## office name ##
    Label(total_frame, text="   اسم المكتب", font=("Helvetica", 13), bg=bottom_color).place(x=145, y=70)
    #office_name_entry = Entry(total_frame, font=("Helvetica", 13), width=10, borderwidth=2)
    #office_name_entry.place(x = 18, y = 70)
    cur.execute("SELECT name FROM office_names")
    office_values = list(map(lambda item: item[0], cur.fetchall()))
    office_compo = ttk.Combobox(total_frame, width=15, values=office_values)
    office_compo.place(x = 18, y = 70)
    #office_compo.current(0)

    button_frame = Frame(prePrinted_window, bg=bottom_color)
    button_frame.pack(fill=X)

    submit_button = Button(button_frame, text="اطبع الفاتورة", command=lambda: 
                                            generate_docx(prePrinted_window, final_total_entry, office_compo), padx=50)
    submit_button.pack(side=BOTTOM)

    prePrinted_window.bind("<Return>", lambda event: submit_button.invoke())

    ## Get Default printer name ##
    printer_name = win32print.GetDefaultPrinter()
    Label(prePrinted_window, text="Default Printer:  " + printer_name, bg=bottom_color,
             anchor=W).pack(side=BOTTOM, fill=X)

## Delete real item ##
def delete_real_item():
    answer = messagebox.askyesno("حذف عنصر", "هل تريد حذف العناصر المحددة؟")
    if answer:
        selection = items_tree.selection()
        for item in selection:
            items_tree.delete(item)
            cur.execute("DELETE FROM items where id = ?", (item, ))
            conn.commit()

def select_searched_item(search_entry):
    text = search_entry.get()
    childeren = items_tree.get_children()
    for child in childeren:
        items_tree.selection_remove(child)
    for child in childeren:
        if text in items_tree.item(child, "values")[2]:
            items_tree.selection_add(child)
    items_tree.see(items_tree.selection()[0])
    search_entry.delete(0, END)
    
## Create print bill command to Bill menue ##
bill_menu.add_command(label="اطبع الفاتورة .. (Ctrl-P)", command=open_prePrinted_window)

## Bind Ctrl-P to open pre-print window ##
root.bind("<Control-Key-P>", lambda event: open_prePrinted_window())
root.bind("<Control-Key-p>", lambda event: open_prePrinted_window())
#root.bind("<Control-Key-ح>", lambda event: open_prePrinted_window())

## Bind Ctrl-N to Add item ##
root.bind("<Control-Key-N>", lambda event: open_add_item_window())
root.bind("<Control-Key-n>", lambda event: open_add_item_window())
#root.bind("<Control-Key-ى>", lambda event: open_add_item_window())

## Bind Ctrl-del to delete items ##
root.bind("<Control-Key-Delete>", lambda event: delete_real_item())

## Create Quit command to items menu ##
item_menu.add_separator()
item_menu.add_command(label="انهاء البرنامج", command=end_program)


root.mainloop()