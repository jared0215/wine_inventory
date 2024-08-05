# views.py
import tkinter as tk
from tkinter import ttk, messagebox
from models import Database
from styles import apply_theme
import logging

logging.basicConfig(level=logging.INFO)

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

        # Wine Name Entry
        self.name_label = ttk.Label(self.add_wine_window, text="Wine Name")
        self.name_label.pack(pady=5)
        self.name_entry = ttk.Entry(self.add_wine_window)
        self.name_entry.pack(pady=5)

        # Wine Type Dropdown
        self.type_label = ttk.Label(self.add_wine_window, text="Wine Type")
        self.type_label.pack(pady=5)
        self.type_combobox = ttk.Combobox(self.add_wine_window, values=self.db.get_types())
        self.type_combobox.pack(pady=5)

        # Wine Year / Vintage Entry
        self.year_label = ttk.Label(self.add_wine_window, text="Year")
        self.year_label.pack(pady=5)
        self.year_entry = ttk.Entry(self.add_wine_window)
        self.year_entry.pack(pady=5)

        # Wine Region Dropdown
        self.region_label = ttk.Label(self.add_wine_window, text="Region")
        self.region_label.pack(pady=5)
        self.region_combobox = ttk.Combobox(self.add_wine_window, values=self.db.get_regions())
        self.region_combobox.pack(pady=5)

        # Wine Price Entry
        self.price_label = ttk.Label(self.add_wine_window, text="Price")
        self.price_label.pack(pady=5)
        self.price_entry = ttk.Entry(self.add_wine_window)
        self.price_entry.pack(pady=5)

        # Wine Quantity Entry
        self.quantity_label = ttk.Label(self.add_wine_window, text="Quantity")
        self.quantity_label.pack(pady=5)
        self.quantity_entry = ttk.Entry(self.add_wine_window)
        self.quantity_entry.pack(pady=5)

        # Save Wine Button
        self.save_button = ttk.Button(self.add_wine_window, text="Save", command=self.save_wine)
        self.save_button.pack(pady=10)

    def save_wine(self):
        name = self.name_entry.get()
        wine_type = self.type_combobox.get()
        year = self.year_entry.get()
        region = self.region_combobox.get()
        price = self.price_entry.get()
        quantity = self.quantity_entry.get()

        # Simple validation
        if not name or not wine_type or not year.isdigit() or not price.replace('.', '', 1).isdigit() or not quantity.isdigit() or not region:
            messagebox.showerror("Error", "Please fill in all fields correctly.")
            return

        year = int(year)
        price = float(price)
        quantity = int(quantity)

        try:
            type_id = self.db.get_id_from_name('types', wine_type)
            region_id = self.db.get_id_from_name('regions', region)

            with self.db.connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO wines (name, type_id, year, region_id, price, quantity) VALUES (%s, %s, %s, %s, %s, %s)",
                    (name, type_id, year, region_id, price, quantity)
                )
            self.db.connection.commit()
            messagebox.showinfo("Success", f"{name} added successfully!")
            self.add_wine_window.destroy()
        except Exception as e:
            logging.error(f"Error saving wine: {e}")
            messagebox.showerror("Database Error", "An error occurred while saving the wine.")

    def update_wine(self):
        # Implement update wine functionality here
        pass

    def delete_wine(self):
        # Implement delete wine functionality here
        pass

    def search_wine(self):
        # Implement search wine functionality here
        pass
    
    def view_wines(self):
        # Create a new window to display the wine list
        self.view_wines_window = tk.Toplevel(self.root)
        self.view_wines_window.title("Wine List")

        # Create a Treeview to display the wines
        columns = ("Name", "Type", "Year", "Region", "Price", "Quantity")
        self.tree = ttk.Treeview(self.view_wines_window, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, minwidth=0, width=100)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Fetch the wine data from the database using get_all_wines
        wines = self.db.get_all_wines()  
        for wine in wines:
            self.tree.insert("", tk.END, values=(wine['name'], wine['type_name'], wine['year'], wine['region_name'], wine['price'], wine['quantity']))

    def close_db_connection(self):
        self.db.close_connection()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = WineInventoryApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close_db_connection)
    root.mainloop()
