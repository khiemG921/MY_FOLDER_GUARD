import os
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from core.main_window import Main_Window
from core.password_evaluation import evaluate_password
from core.face_identification import identify_face

class Login_Window:
    def __init__(self, root):
        self.root = root
        self.root.title("My Data Guard - Login")
        self.root.geometry("400x200")
        self.root.resizable(False, False)

        # Check if the password file exists
        if os.path.exists("./data/key/password_key.txt"):
            # If the file exists, display the login interface
            self.show_login_page()
        else:
            # If the file does not exist, display the password creation interface
            self.show_create_password_page()


    def show_login_page(self):
        # Clear previous widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        # Password Label
        password_label = tk.Label(frame, text="Password:", font=("Arial", 10))
        password_label.grid(row=0, column=0, sticky="e", padx=(0, 10))

        # Password Entry
        self.password_entry = tk.Entry(frame, width=30, show="*", font=("Arial", 10))
        self.password_entry.grid(row=0, column=1, pady=10)

        # "Forgot Password?" Link
        forgot_password_label = tk.Label(frame, text="Forgot password?", fg="blue", cursor="hand2", font=("Arial", 8, "underline"))
        forgot_password_label.grid(row=1, column=0, columnspan=2, sticky="w", padx=(0, 10))
        forgot_password_label.bind("<Button-1>", self.forgot_password)  # Bind event for forgot password link

        # Buttons Frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        # Face ID Button
        face_id_button = tk.Button(button_frame, text="Face ID", width=10, command=self.face_id_login, font=("Arial", 10))
        face_id_button.grid(row=0, column=0, padx=10)

        # OK Button
        ok_button = tk.Button(button_frame, text="OK", width=10, command=self.check_password, bg="#4da6ff", fg="white", font=("Arial", 10, "bold"))
        ok_button.grid(row=0, column=1, padx=10)

        # Cancel Button
        cancel_button = tk.Button(button_frame, text="CANCEL", width=10, command=self.root.quit, font=("Arial", 10))
        cancel_button.grid(row=0, column=2, padx=10)


    def show_create_password_page(self):
        # Clear previous widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        self.recommend_password = None

        # Create New Password Label
        new_password_label = tk.Label(frame, text="Create a new password:", font=("Arial", 10))
        new_password_label.grid(row=0, column=0, sticky="e", padx=(0, 10))

        # New Password Entry (mandatory)
        self.new_password_entry = tk.Entry(frame, width=30, show="*", font=("Arial", 10))
        self.new_password_entry.grid(row=0, column=1, pady=10)

        # Bind event to check password strength on input
        self.new_password_entry.bind("<FocusOut>", self.on_password_entry)

        # Confirm Password Label
        confirm_password_label = tk.Label(frame, text="Confirm your password:", font=("Arial", 10))
        confirm_password_label.grid(row=1, column=0, sticky="e", padx=(0, 10))

        # Confirm Password Entry (mandatory) - initially disabled
        self.confirm_password_entry = tk.Entry(frame, width=30, show="*", font=("Arial", 10))
        self.confirm_password_entry.grid(row=1, column=1, pady=10)

        # Password Strength Label (placed right below Confirm Password Entry)
        self.password_strength_label = tk.Label(self.root, text="", font=("Arial", 9))
        self.password_strength_label.place(x=80, y=100)  # Adjusted to appear below confirm password

        # Add icon for refresh button
        refresh_icon = Image.open("./assets/rotate-right.png").resize((15, 15))
        self.refresh_icon = ImageTk.PhotoImage(refresh_icon)

        self.refresh_button = tk.Button(self.root, image=self.refresh_icon, command=self.refresh_recommendation, bd=0)
        self.refresh_button.place(x=350, y=100)
        self.refresh_button.config(state="disabled")  # Disabled initially

        # Add icon for copy button
        copy_icon = Image.open("./assets/copy-alt.png").resize((15, 15))
        self.copy_icon = ImageTk.PhotoImage(copy_icon)

        self.copy_button = tk.Button(self.root, image=self.copy_icon, command=self.copy_password, bd=0)
        self.copy_button.place(x=370, y=100)
        self.copy_button.config(state="disabled")  # Disabled initially

        # Buttons Frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        # OK Button
        self.ok_button = tk.Button(button_frame, text="OK", width=10, command=self.create_password, bg="#4da6ff", fg="white", font=("Arial", 10, "bold"), state="disabled")
        self.ok_button.grid(row=0, column=0, padx=10)

        # Cancel Button
        self.cancel_button = tk.Button(button_frame, text="CANCEL", width=10, command=self.root.quit, font=("Arial", 10))
        self.cancel_button.grid(row=0, column=1, padx=10)


    def check_password(self):
        password = self.password_entry.get()
        # Check the password in the file
        with open("./data/key/password_key.txt", "r") as file:
            saved_password = file.read().strip()
            if password == saved_password:
                self.open_main_window()
            else:
                messagebox.showerror("Login", "INCORRECT PASSWORD!")


    def on_password_entry(self, event):
        new_password = self.new_password_entry.get().strip()

        # Check password strength
        is_strong, self.recommend_password = evaluate_password(new_password)

        if is_strong:
            self.password_strength_label.config(text="Good password.", fg="#60A500", font=("Arial", 12, "bold"))
            self.ok_button.config(state='normal')  # Enable OK button if the password is strong
            self.refresh_button.config(state='disabled')  # Disable refresh button
            self.copy_button.config(state='disabled')  # Disable copy button
        else:
            self.password_strength_label.config(text=f"Weak password. Recommend: {self.recommend_password}", fg="red", font=("Arial", 10))
            self.ok_button.config(state='disabled')  # Disable OK button if the password is weak
            self.refresh_button.config(state='normal')  # Enable refresh button
            self.copy_button.config(state='normal')  # Enable copy button


    def refresh_recommendation(self):
        # Generate a new recommended password
        _, self.recommend_password = evaluate_password("")  # Call generate_password from evaluate_password
        self.password_strength_label.config(text=f"Weak password. Recommend: {self.recommend_password}", fg="red")


    def create_password(self):
        new_password = self.new_password_entry.get().strip()

        # Check the new password
        is_strong, message = evaluate_password(new_password)

        if is_strong:
            self.password_strength_label.config(text="Good password.", fg="green")
        else:
            self.password_strength_label.config(text=f"Weak password. Recommend: {message}", fg="red")
        
        confirm_password = self.confirm_password_entry.get().strip()

        # Confirm password
        if new_password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        if not new_password or not confirm_password:
            messagebox.showerror("Error", "Please enter and confirm your password!")
            return

        # Save the password to the file
        with open("./data/key/password_key.txt", "w") as file:
            file.write(new_password)

        # Open the main window
        self.open_main_window()


    def copy_password(self):
        # Copy the recommended password to the clipboard
        self.root.clipboard_clear()
        self.root.clipboard_append(self.recommend_password)
                
        # Display "Copied" label
        copied_label = tk.Label(self.root, text="Copied", font=("Arial", 10))
        copied_label.place(x=385, y=98)
        self.root.after(3000, copied_label.destroy)  # Destroy the label after 3 seconds


    def forgot_password(self, event):
        messagebox.showinfo("Forgot Password", "Redirecting to password recovery...")


    def face_id_login(self):
        # Check if Face ID is enabled
        with open("./data/settings/info.txt") as f:
            face_id_on = f.readline().strip()
            
        if face_id_on == "T":
            if identify_face():  # Attempt face recognition
                self.open_main_window()
            else:
                return
        else:
            messagebox.showwarning("Face ID", "Face ID is TURNED OFF.")


    def open_main_window(self):
        # Open the main window after successful login
        self.root.withdraw()
        new_window = tk.Toplevel(self.root)
        main_window = Main_Window(new_window)
        new_window.mainloop()