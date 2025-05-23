from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from db_func import Members                 # Importing Members class from database functions "db_func.py"
from custom_widgets import PrettyButton     # Importing Custom widgets from "custom_wdigets.py"


class MemberMS:
    def __init__(self, root):
        # Main Window
        self.root = root
        self.root.geometry("900x600+100+100")
        self.root.title("Azure Codex: A Library Management System")
        self.root.attributes("-fullscreen", True)
        self.root.resizable(True, True)
        self.root.configure(bg="#202236")
        self.root.minsize(900, 600)

        # Global var for selected Member ID from Table
        self.selected_mem_id = None
        self.search_var = StringVar()

        # UI Setups
        self.setup_ui()
        self.member_preview()

    def setup_ui(self):
        # Banner Row
        banner_frame = Frame(self.root, bg="#202236")
        banner_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        banner_frame.grid_columnconfigure(0, weight=1)
        banner_frame.grid_columnconfigure(1, weight=0)

        # Title Label (left side)
        title_label = Label(banner_frame, text="Manage Members",
                            font=("Segoe UI", 28, "bold"), fg="white", bg="#202236", anchor="w")
        title_label.grid(row=0, column=0, sticky="w", padx=20, pady=20)

        # Banner Image (right side)
        banner_image = Image.open("./assets/banner.png").resize((900, 100))
        self.logo = ImageTk.PhotoImage(banner_image) 
        image_label = Label(banner_frame, image=self.logo, bg="#202236")
        image_label.grid(row=0, column=1, sticky="e")

        # Configuring Grid Layout
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Left Frame
        left_frame = Frame(self.root, bg="#202236")
        left_frame.grid(row=1, column=0, sticky="nsew")
        left_frame.grid_columnconfigure(1, weight=1) 

        # Template for entry box
        def make_label_entry(text, row):
            label = Label(left_frame, text=text, font=("Segoe UI", 18, "bold"), fg="white", bg="#202236")
            label.grid(row=row, column=0, padx=20, pady=15, sticky="w")
            entry = Entry(left_frame, font=("Segoe UI", 15, "bold"), width=20)
            entry.grid(row=row, column=1)
            return entry

        # Making the entry boxes
        self.fnameEntry = make_label_entry("First Name", 0)
        self.snameEntry = make_label_entry("Last Name", 1)
        self.ageEntry = make_label_entry("Age", 2)
        self.emailEntry = make_label_entry("Email", 3)

        # Right Frame
        right_frame = Frame(self.root, width=900)
        right_frame.grid(row=1, column=1, sticky="nsew")
        right_frame.grid_propagate(False) 
        
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_rowconfigure(1, weight=1)
        
        # Entry field and ComboBox for the search functionality
        self.searchBox = ttk.Combobox(right_frame, textvariable=self.search_var,
                                      values=["ID", "First Name", "Last Name", "Age", "Email"], state="readonly")
        self.searchBox.grid(row=0, column=0, sticky="e", padx=4)
        self.searchBox.set("Search By")

        self.searchEntry = Entry(right_frame)
        self.searchEntry.grid(row=0, column=1)

        # Buttons for the table, search and show all
        Button(right_frame, text="Search", width=10, command=self.search_mems).grid(row=0, column=2, padx=4)
        Button(right_frame, text="Show All", width=10, command=self.show_all).grid(row=0, column=3, padx=4, pady=8)

        # the **TABLE** dun dun dun
        self.tree = ttk.Treeview(
            right_frame, height=13,
            columns=('ID', "First Name", "Last Name", "Age", "Email"),
            show='headings'
        )
        self.tree.grid(row=1, column=0, columnspan=4, sticky="nsew")
        
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            if col in ("ID",  "Age"):
                self.tree.column(col, width=50)
            elif col in ("Email"):
                self.tree.column(col, width=250)
            else:
                self.tree.column(col, width=150)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Segoe UI", 18, "bold"))
        style.configure("Treeview", font=("Segoe UI", 15), rowheight=30)

        # Vertical scrollbar
        v_scrollbar = Scrollbar(right_frame, orient=VERTICAL, command=self.tree.yview)
        v_scrollbar.grid(row=1, column=4, sticky="ns")
        self.tree.configure(yscrollcommand=v_scrollbar.set)

        # Horizontal scrollbar
        h_scrollbar = Scrollbar(right_frame, orient=HORIZONTAL, command=self.tree.xview)
        h_scrollbar.grid(row=2, column=0, columnspan=4, sticky="ew")
        self.tree.config(xscrollcommand=h_scrollbar.set)
        
        self.tree.bind("<<TreeviewSelect>>", self.selection)
        
        # The Frame for the Buttons
        btnFrame = Frame(self.root, bg="#202236")
        btnFrame.grid(row=2, column=0, columnspan=2, sticky="ew")
        btnFrame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1) 
        

        # Button template 
        def make_button(text, col, cmd):
            btn = PrettyButton(btnFrame, text=text, command=cmd)
            btn.grid(row=0, column=col, pady=5)
            return btn

        # Making the buttons
        make_button('Refresh Fields', 0, lambda: self.clear(True))
        make_button('Add Member', 1, self.add_mems)
        make_button('Update Member', 2, self.update_mems)
        make_button('Delete Member', 3, self.delete_mem)
        make_button('Main Menu', 4, self.back_to_main)

    # Selection from table function
    def selection(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            row = self.tree.item(selected_item)["values"]
            self.selected_mem_id = row[0]
            self.clear()
            self.fnameEntry.insert(0, row[1])
            self.snameEntry.insert(0, row[2])
            self.ageEntry.insert(0, row[3])
            self.emailEntry.insert(0, row[4])
    
    # Clears empty fields when done
    def clear(self, val=False):
        if val:
            self.tree.selection_remove(self.tree.focus())
        for entry in [self.fnameEntry, self.snameEntry, self.ageEntry, self.emailEntry]:
            entry.delete(0, END)

    # function to show a preview on the table
    def member_preview(self):
        members = Members.fetch_mems()
        self.tree.delete(*self.tree.get_children())
        for member in members:
            self.tree.insert("", END, values=member)

    # function to add members
    def add_mems(self):
        if any(entry.get() == "" for entry in [self.fnameEntry, self.snameEntry, self.ageEntry, self.emailEntry]):
            messagebox.showerror("Error", "All fields are required.")
            return
        try:
            mem = Members(self.fnameEntry.get(), self.snameEntry.get(), self.ageEntry.get(), self.emailEntry.get())
            mem.add_members()
            self.member_preview()
            self.clear()
            messagebox.showinfo('Success', 'Member has been added.')
        except Exception as e:
            messagebox.showerror("Error", e)

    # function to update members
    def update_mems(self):
        if not self.selected_mem_id:
            messagebox.showerror("Error", "Select data to update.")
            return
        try:
            mem = Members(self.fnameEntry.get(), self.snameEntry.get(), self.ageEntry.get(),
                          self.emailEntry.get(), self.selected_mem_id)
            mem.update_members()
            self.member_preview()
            self.clear()
            self.selected_mem_id = None
            messagebox.showinfo('Success', 'Member has been updated.')
        except Exception as e:
            messagebox.showerror("Error", e)

    # function to delete members (ouch)
    def delete_mem(self):
        if not self.selected_mem_id:
            messagebox.showerror("Error", "Select data to delete.")
            return
        try:
            mem = Members(self.fnameEntry.get(), self.snameEntry.get(), self.ageEntry.get(),
                          self.emailEntry.get(), self.selected_mem_id)
            mem.delete_members()
            self.member_preview()
            self.clear()
            self.selected_mem_id = None
            messagebox.showinfo('Success', 'Member has been deleted.')
        except Exception as e:
            messagebox.showerror("Error", e)

    # function for looking up members using different filters
    def search_mems(self):
        field = self.search_var.get()
        query = self.searchEntry.get()
        if field == "Search By":
            messagebox.showerror("Error", "Please select an option.")
            return
        if not query:
            messagebox.showerror("Error", "Enter value to search.")
            return
        try:
            searched_data = Members.search_members(field, query)
            self.tree.delete(*self.tree.get_children())
            for member in searched_data:
                self.tree.insert("", END, values=member)
        except Exception as e:
            messagebox.showerror("Error", e)

    # shows all the members in the preview when button is clicked
    def show_all(self):
        self.member_preview()
        self.searchEntry.delete(0, END)
        self.search_var.set("Search By")
    
    # back to main button functionality
    def back_to_main(self):
        self.root.destroy()
        from mainmenu import MainMenu
        MainMenu.launch()
        
    # launches the window
    @classmethod
    def launch(cls):
        root = Tk()
        root.state("zoomed")
        cls(root)
        root.mainloop()
        
        