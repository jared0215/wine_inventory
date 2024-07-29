import tkinter as tk
from tkinter import ttk, messagebox
from models import Database
from styles import apply_theme

class WineInventoryApp:
    def __init__(self, root):
        self.db = Database()
        self.root = root
        self.root.title("Wine Inventory Management")
        self.root.geometry("800x600")

        # Apply Theme
        apply_theme()

        # Create the main window layout
        self.create_main_window()

    def create_main_window(self):
        self.label = ttk.Label(self.root, text="Welcome to Wine Inventory Management", font=("Helvetica", 16))
        self.label.pack(pady=20)

        self.add_wine_button = ttk.Button(self.root, text="Add Wine", style='Accent.TButton', command=self.add_wine)
        self.add_wine_button.pack(pady=5)

        self.view_wines_button = ttk.Button(self.root, text="View Wine List", style='Accent.TButton', command=self.view_wines)
        self.view_wines_button.pack(pady=5)

        self.update_wine_button = ttk.Button(self.root, text="Update Wine", style='Accent.TButton', command=self.update_wine)
        self.update_wine_button.pack(pady=5)

        self.delete_wine_button = ttk.Button(self.root, text="Delete Wine", style='Accent.TButton', command=self.delete_wine)
        self.delete_wine_button.pack(pady=5)

        self.search_wine_button = ttk.Button(self.root, text="Search Wine", style='Accent.TButton', command=self.search_wine)
        self.search_wine_button.pack(pady=5)

    def add_wine(self):
        # Add Wine Form Window
        self.add_wine_window = tk.Toplevel(self.root)
        self.add_wine_window.title("Add Wine")

        self.name_label = ttk.Label(self.add_wine_window, text="Wine Name")
        self.name_label.pack(pady=5)
        self.name_entry = ttk.Entry(self.add_wine_window)
        self.name_entry.pack(pady=5)

        self.save_button = ttk.Button(self.add_wine_window, text="Save", command=self.save_wine)
        self.save_button.pack(pady=10)

    def save_wine(self):
        name = self.name_entry.get()
        cursor = self.db.connection.cursor()
        cursor.execute("INSERT INTO wines (name) VALUES (%s)", (name,))
        self.db.connection.commit()
        messagebox.showinfo("Success", "Wine added successfully!")
        self.add_wine_window.destroy()

    def view_wines(self):
        # View Wines Window
        self.view_wines_window = tk.Toplevel(self.root)
        self.view_wines_window.title("View Wines")

        wines = self.get_all_wines()

        for wine in wines:
            wine_label = ttk.Label(self.view_wines_window, text=str(wine))
            wine_label.pack(pady=5)

    def update_wine(self):
        # Implement update wine functionality here
        pass

    def delete_wine(self):
        # Implement delete wine functionality here
        pass

    def search_wine(self):
        # Implement search wine functionality here
        pass

    def get_all_wines(self):
        cursor = self.db.connection.cursor()
        cursor.execute("""
            SELECT wines.name, types.type_name, wines.year, wines.price, wines.quantity, regions.region_name
            FROM wines
            JOIN types ON wines.type_id = types.id
            JOIN regions ON wines.region_id = regions.id
        """)
        return cursor.fetchall()

    def close_db_connection(self):
        self.db.close_connection()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = WineInventoryApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close_db_connection)
    root.mainloop()
