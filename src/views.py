import tkinter as tk
from tkinter import messagebox
from src.models import Database

class WineInventoryApp:
    def __init__(self, root):
        self.db = Database()
        self.root = root
        self.root.title("Wine Inventory Management")

        # Create the main window layout
        self.create_main_window()

    def create_main_window(self):
        self.label = tk.Label(self.root, text="Welcome to Wine Inventory Management")
        self.label.pack(pady=10)

        self.add_wine_button = tk.Button(self.root, text="Add Wine", command=self.add_wine)
        self.add_wine_button.pack(pady=5)

    def add_wine(self):
        # Add Wine Form Window
        self.add_wine_window = tk.Toplevel(self.root)
        self.add_wine_window.title("Add Wine")

        self.name_label = tk.Label(self.add_wine_window, text="Wine Name")
        self.name_label.pack(pady=5)
        self.name_entry = tk.Entry(self.add_wine_window)
        self.name_entry.pack(pady=5)

        # Continue adding more fields like year, price, etc.

        self.save_button = tk.Button(self.add_wine_window, text="Save", command=self.save_wine)
        self.save_button.pack(pady=10)

    def save_wine(self):
        name = self.name_entry.get()
        # Retrieve other field values

        cursor = self.db.connection.cursor()
        cursor.execute("INSERT INTO wines (name) VALUES (%s)", (name,))
        self.db.connection.commit()
        messagebox.showinfo("Success", "Wine added successfully!")
        self.add_wine_window.destroy()

    def close_db_connection(self):
        self.db.close_connection()

if __name__ == "__main__":
    root = tk.Tk()
    app = WineInventoryApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close_db_connection)
    root.mainloop()
