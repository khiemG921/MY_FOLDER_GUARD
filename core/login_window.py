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

        # Kiểm tra xem file mật khẩu có tồn tại không
        if os.path.exists("./data/key/password_key.txt"):
            # Nếu file tồn tại thì hiển thị giao diện đăng nhập
            self.show_login_page()
        else:
            # Nếu file không tồn tại thì hiển thị giao diện tạo mật khẩu
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
        forgot_password_label.bind("<Button-1>", self.forgot_password)

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

        # New Password Entry (bắt buộc)
        self.new_password_entry = tk.Entry(frame, width=30, show="*", font=("Arial", 10))
        self.new_password_entry.grid(row=0, column=1, pady=10)

        # Bind sự kiện để kiểm tra mật khẩu khi nhập vào
        self.new_password_entry.bind("<FocusOut>", self.on_password_entry)

        # Confirm Password Label
        confirm_password_label = tk.Label(frame, text="Confirm your password:", font=("Arial", 10))
        confirm_password_label.grid(row=1, column=0, sticky="e", padx=(0, 10))

        # Confirm Password Entry (bắt buộc) - ban đầu khóa
        self.confirm_password_entry = tk.Entry(frame, width=30, show="*", font=("Arial", 10))
        self.confirm_password_entry.grid(row=1, column=1, pady=10)

        # Password Strength Label (đặt ngay dưới Confirm Password Entry)
        self.password_strength_label = tk.Label(self.root, text="", font=("Arial", 9))
        self.password_strength_label.place(x=80, y=100)  # Update vị trí phù hợp dưới confirm password

        # Thêm icon cho nút làm mới (refresh)
        refresh_icon = Image.open("./assets/rotate-right.png").resize((15, 15))
        self.refresh_icon = ImageTk.PhotoImage(refresh_icon)

        self.refresh_button = tk.Button(self.root, image=self.refresh_icon, command=self.refresh_recommendation, bd=0)
        self.refresh_button.place(x=350, y=100)
        self.refresh_button.config(state="disabled")

        # Thêm icon cho nút sao chép (copy)
        copy_icon = Image.open("./assets/copy-alt.png").resize((15, 15))
        self.copy_icon = ImageTk.PhotoImage(copy_icon)

        self.copy_button = tk.Button(self.root, image=self.copy_icon, command=self.copy_password, bd=0)
        self.copy_button.place(x=370, y=100)
        self.copy_button.config(state="disabled")

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
        # Kiểm tra mật khẩu trong file
        with open("./data/key/password_key.txt", "r") as file:
            saved_password = file.read().strip()
            if password == saved_password:
                self.open_main_window()
            else:
                messagebox.showerror("Login", "Incorrect password!")


    def on_password_entry(self, event):
        new_password = self.new_password_entry.get().strip()

        # Kiểm tra độ mạnh của mật khẩu
        is_strong, self.recommend_password = evaluate_password(new_password)

        if is_strong:
            self.password_strength_label.config(text="Good password.", fg="#60A500", font=("Arial", 12, "bold"))
            self.ok_button.config(state='normal')  # Kích hoạt nút OK khi mật khẩu mạnh
            self.refresh_button.config(state='disabled')  # Vô hiệu hóa nút làm mới
            self.copy_button.config(state='disabled') # Vô hiệu hóa nút sao chép
        else:
            self.password_strength_label.config(text=f"Weak password. Recommend: {self.recommend_password}", fg="red", font=("Arial", 10))
            self.ok_button.config(state='disabled')  # Khóa nút OK khi mật khẩu yếu
            self.refresh_button.config(state='normal')  # Kích hoạt nút làm mới khi mật khẩu yếu
            self.copy_button.config(state='normal') # Kích hoạt nút sao chép khi mật khẩu yếu


    def refresh_recommendation(self):
        # Tạo mật khẩu đề nghị mới
        _, self.recommend_password = evaluate_password("")  # Gọi lại generate_password từ evaluate_password
        self.password_strength_label.config(text=f"Weak password. Recommend: {self.recommend_password}", fg="red")


    def create_password(self):
        new_password = self.new_password_entry.get().strip()

        # Kiểm tra mật khẩu mới
        is_strong, message = evaluate_password(new_password)

        if is_strong:
            self.password_strength_label.config(text="Good password.", fg="green")
        else:
            self.password_strength_label.config(text=f"Weak password. Recommend: {message}", fg="red")
        
        confirm_password = self.confirm_password_entry.get().strip()

        # Xác nhận mật khẩu
        if new_password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        if not new_password or not confirm_password:
            messagebox.showerror("Error", "Please enter and confirm your password!")
            return

        # Lưu mật khẩu vào file
        with open("./data/key/password_key.txt", "w") as file:
            file.write(new_password)

        # Chuyển đến Main Window
        self.open_main_window()


    def copy_password(self):
        # Sao chép mật khẩu đề xuất vào clipboard
        self.root.clipboard_clear()
        self.root.clipboard_append(self.recommend_password)
                
        # Copied Label
        copied_label = tk.Label(self.root, text="Copied", font=("Arial", 10))
        copied_label.place(x=385, y=98)
        self.root.after(3000, copied_label.destroy)


    def forgot_password(self, event):
        messagebox.showinfo("Forgot Password", "Redirecting to password recovery...")


    def face_id_login(self):
        with open("./data/settings/info.txt") as f:
            face_id_on = f.readline().strip()
            
        if face_id_on == "T":
            if identify_face():
                self.open_main_window()
            else:
                return
        else:
            messagebox.showwarning("Face ID", "Face ID is turned off.")


    def open_main_window(self):
        self.root.destroy()
        main_root = tk.Tk()
        main_app = Main_Window(main_root)
        main_root.mainloop()