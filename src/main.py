from views import WineInventoryApp
import tkinter as tk

def main():
    root = tk.Tk()
    app = WineInventoryApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close_db_connection)
    root.mainloop()

if __name__ == "__main__":
    main()
