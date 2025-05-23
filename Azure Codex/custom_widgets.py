import tkinter as tk

class PrettyButton(tk.Button):
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            bg="#7d8bae",
            fg="white",
            font=("Segoe UI", 18, "bold"),
            width=16,
            activebackground="#202236",
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            highlightthickness=0,
            **kwargs
        )