import tkinter as tk

def main():
    root = tk.Tk()
    root.title("Wine Inventory Management")
    root.geometry("800x600")

    label = tk.Label(root, text="Welcome to Wine Inventory Management")
    label.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
