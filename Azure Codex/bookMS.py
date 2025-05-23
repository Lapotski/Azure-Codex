from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from db_func import Books                   # Importing Books class from database functions "db_func.py"
from custom_widgets import PrettyButton     # Importing Custom widgets from "custom_wdigets.py"

class BookMS:
    def __init__(self, root):
        # Initialize main window
        self.root = root
        self.root.geometry("900x600+100+100")
        self.root.title("Azure Codex: A Library Management System")
        self.root.attributes("-fullscreen", True)
        self.root.resizable(True, True)
        self.root.configure(bg="#202236")
        self.root.minsize(900, 600)

        # Global var for selected Book ID from Table
        self.selected_book_id = None
        self.search_var = StringVar()

        # UI setups
        self.setup_ui()
        self.book_preview()

    def setup_ui(self):
        # Banner Row
        banner_frame = Frame(self.root, bg="#202236")
        banner_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        banner_frame.grid_columnconfigure(0, weight=1)
        banner_frame.grid_columnconfigure(1, weight=0)

        # Title Label (left side)
        title_label = Label(banner_frame, text="Manage Books",
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
        self.titleEntry = make_label_entry("Title", 0)
        self.authorEntry = make_label_entry("Author", 1)
        self.totalEntry = make_label_entry("Total Copies", 2)
        self.availableEntry = make_label_entry("Available", 3)

        # Right Frame
        right_frame = Frame(self.root, width=900)
        right_frame.grid(row=1, column=1, sticky="nsew")
        right_frame.grid_propagate(False)

        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_rowconfigure(1, weight=1)

        # Entry field and ComboBox for the search functionality
        self.searchBox = ttk.Combobox(right_frame, textvariable=self.search_var,
                                      values=["ID", "Title", "Author"], state="readonly")
        self.searchBox.grid(row=0, column=0, sticky="e", padx=4)
        self.searchBox.set("Search By")

        self.searchEntry = Entry(right_frame)
        self.searchEntry.grid(row=0, column=1)

        # Buttons for the table, search and show all
        Button(right_frame, text="Search", width=10, command=self.search_books).grid(row=0, column=2, padx=4)
        Button(right_frame, text="Show All", width=10, command=self.show_all).grid(row=0, column=3, padx=4, pady=8)

        # the **TABLE** dun dun dun
        self.tree = ttk.Treeview(
            right_frame,
            height=13,
            columns=('ID', "Title", "Author", "Total", "Available"),
            show='headings'
        )
        self.tree.grid(row=1, column=0, columnspan=4, sticky="nsew")

        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            if col == "ID":
                self.tree.column(col, width=50, anchor="center")
            elif col == "Title":
                self.tree.column(col, width=600, stretch=False, anchor="w") 
            elif col in ("Total", "Available"):
                self.tree.column(col, width=100, anchor="center")
            else:
                self.tree.column(col, width=200, anchor="w")

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Segoe UI", 18, "bold"))
        style.configure("Treeview", font=("Segoe UI", 15), rowheight=30)

        # Vertical scrollbar
        v_scrollbar = Scrollbar(right_frame, orient=VERTICAL, command=self.tree.yview)
        v_scrollbar.grid(row=1, column=4, sticky="ns")
        self.tree.config(yscrollcommand=v_scrollbar.set)

        # Horizontal scrollbar
        h_scrollbar = Scrollbar(right_frame, orient=HORIZONTAL, command=self.tree.xview)
        h_scrollbar.grid(row=2, column=0, columnspan=4, sticky="ew")
        self.tree.config(xscrollcommand=h_scrollbar.set)

        self.tree.bind("<<TreeviewSelect>>", self.selection)

        # The Frame for Buttons
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
        make_button('Add Book', 1, self.add_books)
        make_button('Update Book', 2, self.update_books)
        make_button('Delete Book', 3, self.delete_book)
        make_button('Main Menu', 4, self.back_to_main)

    # Selection from table function
    def selection(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            row = self.tree.item(selected_item)["values"]
            self.selected_book_id = row[0]
            self.clear()
            self.titleEntry.insert(0, row[1])
            self.authorEntry.insert(0, row[2])
            self.totalEntry.insert(0, row[3])
            self.availableEntry.insert(0, row[4])

    # Clears empty fields when done
    def clear(self, val=False):
        if val:
            self.tree.selection_remove(self.tree.focus())
        for entry in [self.titleEntry, self.authorEntry, self.totalEntry, self.availableEntry]:
            entry.delete(0, END)

    # function to show a preview on the table
    def book_preview(self):
        books = Books.fetch_books()
        self.tree.delete(*self.tree.get_children())
        for book in books:
            self.tree.insert("", END, values=book)

    # function to add books
    def add_books(self):
        if any(entry.get() == "" for entry in [self.titleEntry, self.authorEntry, self.totalEntry, self.availableEntry]):
            messagebox.showerror("Error", "All fields are required.")
            return
        try:
            book = Books(self.titleEntry.get(), self.authorEntry.get(), self.totalEntry.get(), self.availableEntry.get())
            book.add_books()
            self.book_preview()
            self.clear()
            messagebox.showinfo('Success', 'Book has been added.')
        except Exception as e:
            messagebox.showerror("Error", e)

    # function to update books
    def update_books(self):
        if not self.selected_book_id:
            messagebox.showerror("Error", "Select data to update.")
            return
        try:
            book = Books(self.titleEntry.get(), self.authorEntry.get(), self.totalEntry.get(),
                          self.availableEntry.get(), self.selected_book_id)
            book.update_books()
            self.book_preview()
            self.clear()
            self.selected_book_id = None
            messagebox.showinfo('Success', 'Book has been updated.')
        except Exception as e:
            messagebox.showerror("Error", e)

    # function to delete books (ouch)
    def delete_book(self):
        if not self.selected_book_id:
            messagebox.showerror("Error", "Select data to delete.")
            return
        try:
            book = Books(self.titleEntry.get(), self.authorEntry.get(), self.totalEntry.get(),
                          self.availableEntry.get(), self.selected_book_id)
            book.delete_books()
            self.book_preview()
            self.clear()
            self.selected_book_id = None
            messagebox.showinfo('Success', 'Book has been deleted.')
        except Exception as e:
            messagebox.showerror("Error", e)

    # function for looking up books using different filters
    def search_books(self):
        field = self.search_var.get()
        query = self.searchEntry.get()
        if field == "Search By":
            messagebox.showerror("Error", "Please select an option.")
            return
        if not query:
            messagebox.showerror("Error", "Enter value to search.")
            return
        try:
            searched_data = Books.search_books(field, query)
            self.tree.delete(*self.tree.get_children())
            for book in searched_data:
                self.tree.insert("", END, values=book)
        except Exception as e:
            messagebox.showerror("Error", e)

    # shows all the books in the preview when button is clicked
    def show_all(self):
        self.book_preview()
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
