from views import WineInventoryApp
import tkinter as tk
from models import Database  # Assuming Database is in src/models.py

def setup_database():
    db = Database()
    db.create_tables()  # This creates the tables in your database
    db.populate_from_json('webScraper/wine_regions.json')  # This populates the tables with data from your JSON file
    db.close_connection()  # This closes the database connection

def main():
    root = tk.Tk()
    app = WineInventoryApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close_db_connection)
    root.mainloop()

if __name__ == "__main__":
    setup_database()  # Set up the database first
    main()  # Then start the GUI application
