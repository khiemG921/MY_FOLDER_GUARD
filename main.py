import tkinter as tk
from core.login_window import Login_Window

def main():
    root = tk.Tk()
    root.resizable(False, False)  # Prevent resizing

    app = Login_Window(root)

    root.mainloop()

if __name__ == "__main__":
    main()