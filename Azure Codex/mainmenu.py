import tkinter as tk
from PIL import Image, ImageTk
from custom_widgets import PrettyButton
import memberMS,  bookMS, borrowSystem

class MainMenu:
    # Initializing main window
    def __init__(self, root):
        self.root = root
        self.root.title("Azure Codex: A Library Management System")
        self.root.attributes("-fullscreen", True)
        self.root.geometry("900x600")
        self.root.resizable(True, True)
        self.root.minsize(900, 600)

        # Loading the background image
        self.original_bg = Image.open("./assets/mm_bg.png")
        self.bg_image = None
        self.bg_label = tk.Label(self.root)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.root.bind("<Configure>", self.resize_background)

        # Calls the create_widgets function to create the buttons and heading for the main menu
        self.create_widgets()

    # Makes the bg resizeable
    def resize_background(self, event):
        if event.widget == self.root:
            new_width = event.width
            new_height = event.height
            resized = self.original_bg.resize((new_width, new_height), Image.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(resized)
            self.bg_label.configure(image=self.bg_image)
            self.bg_label.image = self.bg_image  

    # Function to contain all my widgets
    def create_widgets(self):
        main_frame = tk.Frame(self.root, bg="#e8ccc7", bd=2, relief="flat")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        label = tk.Label(
            main_frame,
            text="Azure Codex",
            font=("Segoe UI", 28, "bold"),
            bg="#e8ccc7",
            fg="#202236"
        )
        label.pack(pady=(40, 30))

        # Button container
        btn_container = tk.Frame(main_frame, bg="#e8ccc7")
        btn_container.pack()

        btn_width = 25 

        # MainMenu Buttons
        PrettyButton(btn_container, text="Manage Books", command=self.manage_books).pack(padx=8, pady=8, ipadx=10, ipady=5, fill="x")
        PrettyButton(btn_container, text="Manage Members", command=self.manage_members).pack(padx=8, pady=8, ipadx=10, ipady=5, fill="x")
        PrettyButton(btn_container, text="Lending System", command=self.borrow_system).pack(padx=8, pady=8, ipadx=10, ipady=5, fill="x")
        PrettyButton(btn_container, text="Exit", command=self.exit_app).pack(padx=8, pady=8, ipadx=10, ipady=5, fill="x")

        for child in btn_container.winfo_children():
            child.configure(width=btn_width)
            
        credits = tk.Label(
            self.root,
            text="© 2025 Azure Codex | Developed by Kyla Dessirei Dequito",
            font=("Segoe UI", 10),
            bg="#e8ccc7", 
            fg="#413F3F"
        )
        credits.place(relx=0.0, rely=1.0, anchor='sw', x=10, y=-10)


    # Button Functionalities
    def manage_books(self):
        self.root.destroy()
        bookMS.BookMS.launch()

    def manage_members(self):
        self.root.destroy()
        memberMS.MemberMS.launch()

    def borrow_system(self):
        self.root.destroy()
        borrowSystem.BorrowMS.launch()

    def exit_app(self):
        self.root.destroy()

    # Launches window, used mainly to for import purposes
    @classmethod
    def launch(cls):
        root = tk.Tk()
        root.state("zoomed")
        cls(root)
        root.mainloop()

# Launch the app
if __name__ == "__main__":
    root = tk.Tk()
    root.state("zoomed")
    app = MainMenu(root)
    root.mainloop()
    
    
    
    
    
    
    