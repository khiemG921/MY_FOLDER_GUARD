import os
import tkinter as tk
from PIL import Image, ImageTk
from core.folder_protection import *
from core.password_evaluation import *
from core.face_identification import capture_face
from tkinter import ttk, filedialog, messagebox

CHECKED_BOX_PATH = "./assets/checked.png"
UNCHECKED_BOX_PATH = "./assets/unchecked.png"
SEARCH_GLASS_PATH = "./assets/magnifying-glass.png"

class Search_Bar():
    def __init__(self, root):
        self.folder_table = None
        self.search_img = ImageTk.PhotoImage(Image.open(SEARCH_GLASS_PATH).resize((20, 20)))


        # Frame to hold the entire bar
        self.top_frame = tk.Frame(root, padx=10, pady=10, width=650, height=100)
        self.top_frame.pack_propagate(0)  # Prevents the frame from shrinking to fit its contents
        self.top_frame.pack(fill="x")  # Adjusted to 'x' to fill horizontally, not vertically

        # Search Entry
        self.search_entry = tk.Entry(self.top_frame, width=45, font=("Arial", 12), bd=2, relief="groove")
        self.search_entry.place(x=10, y=15)

        # Search icon (using text for simplicity, you can replace it with an image)
        self.search_icon = tk.Button(self.top_frame, image=self.search_img, bd=0, font=("Arial", 12), padx=2, pady=2,command=lambda: self.search_folder(root))
        self.search_icon.place(x=425, y=15)

        # Add button
        self.add_button = tk.Button(self.top_frame, text="+ ADD", bd=0, bg="#3cb0fd", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5, command=self.open_folder_dialog)
        self.add_button.place(x=460, y=5)

        # Canvas to group the status dot and toggle button
        self.toggle_frame = tk.Canvas(self.top_frame, width=100, height=50, highlightthickness=0)
        self.toggle_frame.place(x=550, y=5)

        # Status dot (green/red depending on ON/OFF)
        self.status_dot = tk.Canvas(self.toggle_frame, width=15, height=15, bg="green", highlightthickness=0)
        self.status_dot.place(x=15, y=12)  # Adjusted the position within the toggle_frame

        # ON-OFF Toggle button
        self.toggle_button = tk.Button(self.toggle_frame, text="ON", font=("Arial", 12, "bold"), bd=0, command=self.toggle_status, fg="green")
        self.toggle_button.place(x=30, y=5)  # Positioned next to the status dot

        # Bind hover events to show and hide the border
        self.toggle_frame.bind("<Enter>", self.show_border)
        self.toggle_frame.bind("<Leave>", self.hide_border)

        # Bind hover events to make lighter and default the "+ ADD" button
        self.add_button.bind("<Enter>", self.make_lighter)
        self.add_button.bind("<Leave>", self.make_default)


    def toggle_status(self):
        # Toggle between ON and OFF
        if self.toggle_button.cget("text") == "ON":
            self.toggle_button.config(text="OFF", fg="red")
            self.status_dot.config(bg="red")
            self.disable_widgets()  # Disable all relevant widgets
        else:
            self.toggle_button.config(text="ON", fg="green")
            self.status_dot.config(bg="green")
            self.enable_widgets()  # Enable all relevant widgets


    # Function to open the "Browse for folder" dialog and insert into the table
    def open_folder_dialog(self):
        folder_selected = filedialog.askdirectory(title="Select a folder to secure")
        if folder_selected:
            self.folder_table.insert_folder(folder_selected)  # Insert the folder into the table


    # Function to search for folder
    def search_folder(self, root, event=None):
        folder_path = self.search_entry.get()             # Get the input text
        if folder_path and os.path.isdir(folder_path):    # Check if it's a valid directory
            self.folder_table.insert_folder(folder_path)  # Insert folder into folder_table
        else:
            error_msg = tk.Label(self.top_frame, text="Invalid folder path!", font=("Arial", 12))
            error_msg.place(x=10, y=45)
            root.after(5000, error_msg.destroy)
            

    # Function to show border on hover
    def show_border(self, event):
        self.toggle_frame.create_rectangle(0, 0, 75, 40, outline="blue", width=2)


    # Function to hide border when mouse leaves
    def hide_border(self, event):
        self.toggle_frame.create_rectangle(0, 0, 75, 40, outline="#f0f0f0", width=2)


    def make_lighter(self, event):
        event.widget.configure(bg="#5dc0ff")


    def make_default(self, event):
        event.widget.configure(bg="#3cb0fd", font=("Arial", 12, "bold"))


    def disable_widgets(self):
        self.search_entry.config(state="disabled")      # Disable the search bar
        self.search_icon.config(state="disabled")       # Disable the search button
        self.add_button.config(state="disabled")        # Disable the + ADD button
        self.folder_table.select_all_checkbox.config(state="disabled")  # Disable the Select All checkbox
        self.folder_table.remove_button.config(state="disabled")  # Disable the Remove All button

        # Unbind mouse click events on the folder_table to disable row selection
        self.folder_table.folder_table.unbind("<Button-1>")
        self.folder_table.folder_table.unbind("<ButtonRelease-1>")


    def enable_widgets(self):
        self.search_entry.config(state="normal")        # Re-enable the search bar
        self.search_icon.config(state="normal")         # Re-enable the search button
        self.add_button.config(state="normal")          # Re-enable the + ADD button
        self.folder_table.select_all_checkbox.config(state="normal")  # Re-enable the Select All checkbox
        self.folder_table.remove_button.config(state="normal")  # Re-enable the Remove All button

        # Bind the mouse click events again to enable row selection in the folder_table
        self.folder_table.folder_table.bind("<Button-1>", self.folder_table.on_click_select)
        self.folder_table.folder_table.bind("<ButtonRelease-1>", self.folder_table.on_click_combobox)



class Folder_Table():
    def __init__(self, root):
        # Selected folders will be stored in a dictionary (key=row_id, value=selected or not)
        self.selected_folders = {}

        # Load checkbox images
        self.checked_img = ImageTk.PhotoImage(Image.open(CHECKED_BOX_PATH).resize((20, 20)))
        self.unchecked_img = ImageTk.PhotoImage(Image.open(UNCHECKED_BOX_PATH).resize((20, 20)))

        # Folder list (Location, Protection Method)
        self.folder_table = ttk.Treeview(root, columns=("Location", "Protection Method"), height=8, selectmode='none')
        self.folder_table.heading("#0", text="Select")
        self.folder_table.heading("Location", text="Location")
        self.folder_table.heading("Protection Method", text="Protection Method")
        self.folder_table.column("#0", width=50, anchor='center')
        self.folder_table.column("Location", width=400)
        self.folder_table.column("Protection Method", width=150)
        self.folder_table.pack(fill="both", expand=True, padx=(20, 0), pady=(0, 30))

        # Create a frame to hold the checkbox, label, and the REMOVE button
        self.select_all_frame = tk.Frame(root)
        self.select_all_frame.pack(side="left")  # Adjust the x, y coordinates accordingly

        # Add "Select All" checkbox with images (checked/unchecked)
        self.select_all_var = tk.BooleanVar()
        self.select_all_checkbox = tk.Button(self.select_all_frame, image=self.unchecked_img, command=self.toggle_select_all, bd=0)
        self.select_all_checkbox.pack(side="left", padx=(20, 0), pady=(0, 20))

        # Label for 'Select all'
        self.select_all_label = tk.Label(self.select_all_frame, text="Select all", font=("Arial", 10))
        self.select_all_label.pack(side="left", pady=(0, 20))

        # Bind click events for selecting rows and methods
        self.folder_table.bind("<Button-1>", self.on_click_select)
        self.folder_table.bind("<ButtonRelease-1>", self.on_click_combobox)

        # Add "Remove" button to remove selected rows
        self.remove_button = tk.Button(root, text="REMOVE", bd=0, bg="#3399FE", fg="white", font=("Arial", 10, "bold"), padx=5, pady=5, command=self.remove_selected)
        self.remove_button.pack(side="left", padx=(10, 0), pady=(0, 20))

        # Bind a click event to handle combobox display
        self.remove_button.bind("<Enter>", self.on_enter_remove)
        self.remove_button.bind("<Leave>", self.on_leave_remove)

        # Create the combobox (initially hidden)
        self.combobox = ttk.Combobox(root, values=METHODS, state="readonly")
        self.combobox.bind("<<ComboboxSelected>>", self.on_select_combobox)
        self.combobox.place_forget()  # Hide it initially

        # Bind scrolling events to adjust combobox
        self.folder_table.bind("<MouseWheel>", self.on_scroll)
        self.folder_table.bind("<Configure>", self.on_scroll)  # Also adjust on resize

         # Add label to show item count and protection status
        self.status_label = tk.Label(root, text="", font=("Arial", 10))
        self.status_label.pack(side="right", padx=(0, 20), pady=(0, 20))

        # Update the status label initially
        self.update_status_label()

        # Track selected row
        self.selected_row = None

        # Save the choice of each row
        self.protection_methods = {}


    def insert_folder(self, path):
        # Insert folder with checkbox (unchecked by default)
        row_id = self.folder_table.insert(parent="", index="end", values=(path, "Unprotect"), image=self.unchecked_img)
        self.selected_folders[row_id] = False  # Initialize as unchecked
        # Update status label after inserting a folder
        self.update_status_label()


    def remove_selected(self):
        # Remove selected folders
        for row_id, selected in list(self.selected_folders.items()):
            if selected:
                self.folder_table.delete(row_id)
                del self.selected_folders[row_id]

        # Update status label after removing folders
        self.update_status_label()


    def on_click_combobox(self, event):
        # Check if click is on Protection Method column
        column = self.folder_table.identify_column(event.x)
        row_id = self.folder_table.identify_row(event.y)
        if column == "#2":  # If Protection Method column is clicked
            # Get bounding box for the cell
            bbox = self.folder_table.bbox(row_id, column)
            if bbox:
                # Show combobox at the cell position
                self.combobox.place(x=bbox[0] + self.folder_table.winfo_x(),
                                    y=bbox[1] + self.folder_table.winfo_y(),
                                    width=bbox[2], height=bbox[3])
                self.selected_row = row_id
                
                # Set combobox value to current cell value or use saved value
                self.combobox.set(self.protection_methods.get(row_id, "Unprotect"))  # Default to "Unprotect"
        else:
            # Hide the combobox if clicking outside the Protection Method column
            self.combobox.place_forget()


    def on_select_combobox(self, event):
        # Update the cell value with selected combobox value
        if self.selected_row:
            new_value = self.combobox.get()
            self.protection_methods[self.selected_row] = new_value  # Save choice into the dictionary
            folder_path = self.folder_table.item(self.selected_row, "values")[0]  # Get the folder path

            # Update the table display
            self.folder_table.item(self.selected_row, values=(folder_path, new_value))

            # Update status label after changing protection method
            self.update_status_label()

            # Call the appropriate function based on the selected protection method
            if new_value == "Unprotect":
                unprotect(folder_path)
            elif new_value == "Hide":
                hide(folder_path)
            elif new_value == "Lock":
                lock(folder_path)
            elif new_value == "Read-Only":
                read_only(folder_path)
            elif new_value == "Encrypt":
                encrypt(folder_path)
            elif new_value == "Fully Protect":
                fully_protect(folder_path)


    def on_scroll(self, event):
        # If combobox is visible, move it accordingly
        if self.combobox.winfo_ismapped() and self.selected_row:
            # Get bounding box of the selected row and adjust combobox position
            bbox = self.folder_table.bbox(self.selected_row, "#3")
            if bbox:
                self.combobox.place(x=bbox[0] + self.folder_table.winfo_x(),
                                    y=bbox[1] + self.folder_table.winfo_y(),
                                    width=bbox[2], height=bbox[3])
    

    def toggle_select_all(self):
        # Select or deselect all checkboxes based on "Select All"
        select_all = not self.select_all_var.get()  # Invert the current state
        self.select_all_var.set(select_all)

        # Update the 'Select All' checkbox image
        new_image = self.checked_img if select_all else self.unchecked_img
        self.select_all_checkbox.config(image=new_image)

        for row_id in self.selected_folders:
            self.selected_folders[row_id] = select_all
            new_image = self.checked_img if select_all else self.unchecked_img
            self.folder_table.item(row_id, image=new_image)
            

    def on_click_select(self, event):
        # Handle checkbox click
        region = self.folder_table.identify_region(event.x, event.y)
        column = self.folder_table.identify_column(event.x)
        row_id = self.folder_table.identify_row(event.y)
        if region == "tree":  # Checkbox column
            if row_id:
                # Toggle the checkbox state
                current_state = self.selected_folders.get(row_id, False)
                new_state = not current_state
                self.selected_folders[row_id] = new_state

                # Update checkbox image
                new_image = self.checked_img if new_state else self.unchecked_img
                self.folder_table.item(row_id, image=new_image)

    
    def on_enter_remove(self, event):
        self.remove_button['bg'] = '#395585'  # Màu nền xanh nhạt khi hover
        self.remove_button['fg'] = "white"


    def on_leave_remove(self, event):
        self.remove_button['bg'] = '#3399FE'  # Trở lại màu nền trắng khi rời khỏi nút
        self.remove_button['fg'] = "white"
    

    def update_status_label(self):
        # Count total items and protected items
        total_items = len(self.folder_table.get_children())
        protected_items = sum(1 for row_id in self.folder_table.get_children() 
                              if self.folder_table.item(row_id, "values")[1] != "Unprotect")
        
        # Update the label text
        self.status_label.config(text=f"{total_items} item(s) in total, {protected_items} protected.")



class Home_Page():
    def __init__(self, content_area):
        self.hp_frame = tk.Frame(content_area)

        # Top search bar
        self.search_bar = Search_Bar(self.hp_frame)
        self.folder_table = Folder_Table(self.hp_frame)

        self.search_bar.folder_table = self.folder_table
        self.load_state()

    
    def save_state(self):
        with open("./data/folder_table/folder_state.txt", "w", encoding='utf-8') as f:
            for row_id in self.folder_table.folder_table.get_children():
                # Kiểm tra tag của dòng đó có là checked hay không
                tags = self.folder_table.folder_table.item(row_id, "tags")
                selected = "True" if "checked" in tags else "False"
                folder_path = self.folder_table.folder_table.item(row_id, "values")[0]
                protection_method = self.folder_table.folder_table.item(row_id, "values")[1]
                f.write(f"{selected}|{folder_path}|{protection_method}\n")

    
    def load_state(self):
        try:
            with open('./data/folder_table/folder_state.txt', 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if line:
                        select, path, protecttion_method = line.split('|')
                        if select == 'True':
                            img = self.folder_table.checked_img
                        else:
                            img = self.folder_table.unchecked_img
                        self.folder_table.folder_table.insert('', 'end', values=(path, protecttion_method), image=img)
                        self.folder_table.update_status_label()
        except FileNotFoundError:
            pass

    
    def show(self):
        self.hp_frame.pack(fill="both", expand=True)

    
    def hide(self):
        self.hp_frame.pack_forget()



class Settings_Page:
    def __init__(self, content_area):
        self.load_settings_info()
        self.sp_frame = tk.Frame(content_area)
        
        # Change Password section
        change_password_label = tk.Label(self.sp_frame, text="Change Password:", font=("Arial", 10, "bold"))
        change_password_label.grid(row=0, column=0, sticky="w", pady=10)

        change_password_description = tk.Label(self.sp_frame, text="Create a new master password", font=("Arial", 10))
        change_password_description.grid(row=0, column=1, pady=10)

        current_password_label = tk.Label(self.sp_frame, text="Current Password:")
        current_password_label.grid(row=1, column=1, sticky="w", pady=5)
        self.current_password_entry = tk.Entry(self.sp_frame, show="*")
        self.current_password_entry.grid(row=1, column=2, pady=5)

        new_password_label = tk.Label(self.sp_frame, text="New Password:")
        new_password_label.grid(row=2, column=1, sticky="w", pady=5)
        self.new_password_entry = tk.Entry(self.sp_frame, show="*")
        self.new_password_entry.grid(row=2, column=2, pady=5)

        confirm_password_label = tk.Label(self.sp_frame, text="Confirm Password:")
        confirm_password_label.grid(row=3, column=1, sticky="w", pady=5)
        self.confirm_password_entry = tk.Entry(self.sp_frame, show="*")
        self.confirm_password_entry.grid(row=3, column=2, pady=5)

        # Protection Method section
        protection_method_label = tk.Label(self.sp_frame, text="Protection Method:", font=("Arial", 10, "bold"))
        protection_method_label.grid(row=4, column=0, columnspan=2, sticky="w", pady=10)

        new_item_label = tk.Label(self.sp_frame, text="New item is defaulted by:")
        new_item_label.grid(row=5, column=1, sticky="w", pady=5)

        self.new_item_combobox = ttk.Combobox(self.sp_frame, values=METHODS, state="readonly")
        self.new_item_combobox.set(self.default_protection_method)
        self.new_item_combobox.grid(row=5, column=2, pady=5)

        # Face ID section
        # Load checkbox images
        self.checked_img = ImageTk.PhotoImage(Image.open(CHECKED_BOX_PATH).resize((20, 20)))
        self.unchecked_img = ImageTk.PhotoImage(Image.open(UNCHECKED_BOX_PATH).resize((20, 20)))

        face_id_label = tk.Label(self.sp_frame, text="Face Identification:", font=("Arial", 10, "bold"))
        face_id_label.grid(row=6, column=0, columnspan=2, sticky="w", pady=10) 

        face_id_description = tk.Label(self.sp_frame, text="Turn on Face ID")
        face_id_description.grid(row=7, column=1, sticky="w", pady=10)

        self.face_id_var = tk.BooleanVar()
        self.face_id_var.set(self.face_id_on)
        self.face_id_checkbox = tk.Button(self.sp_frame, image=self.checked_img if self.face_id_on else self.unchecked_img, bd=0, command=self.toggle_face_id)
        self.face_id_checkbox.grid(row=7, column=2, sticky="w", pady=10)

        # Apply button
        self.apply_button = tk.Button(self.sp_frame, text="APPLY", bg="#3399FE", fg="white", font=("Arial", 10, "bold"), padx=20, pady=5, command=self.apply_changes)
        self.apply_button.grid(row=8, column=4, padx=10, pady=20, sticky="e")

        self.sp_frame.pack(fill="both", expand=True)


    def load_settings_info(self):
        with open("./data/settings/info.txt", "r") as f:
            self.face_id_on = False if f.readline() == "F" else True
            self.default_protection_method = f.readline()

        with open("./data/key/password_key.txt", "r") as f:
            self.current_password = f.readline()


    def toggle_face_id(self):
        face_id = not self.face_id_var.get()
        self.face_id_var.set(face_id)

        new_image = self.checked_img if face_id else self.unchecked_img
        self.face_id_checkbox.config(image=new_image)


    def change_password(self):
        new_password = self.new_password_entry.get().strip()
        isStrong, _ = evaluate_password(new_password)
        if self.current_password_entry.get().strip() != self.current_password:
            unlike_current_password_label = tk.Label(self.sp_frame, text="Incorrect current password.", fg="red")
            unlike_current_password_label.grid(row=1, column=4, padx=5, pady=5)
        elif new_password is not None and not isStrong:
            password_strength_label = tk.Label(self.sp_frame, text="Weak password.", fg="red")
            password_strength_label.grid(row=2, column=4, padx=5, pady=5)
        elif self.confirm_password_entry.get().strip() != new_password:
            unlike_new_password_label = tk.Label(self.sp_frame, text="Password do not match.", fg="red")
            unlike_new_password_label.grid(row=3, column=4, padx=5, pady=5)
        else:
            with open("./data/key/password_key.txt", "w") as f:
                f.write(new_password)


    def apply_changes(self):
        # Apply changing password section
        if len(self.current_password_entry.get().strip()) > 0:
            self.change_password()

        # Apply default protection method and face id
        num_imgs = len(os.listdir("./data/facial_images"))
        if self.face_id_var.get() and num_imgs == 0:
            messagebox.showinfo("Face ID", "Create face ID.")
            capture_face()

        with open("./data/settings/info.txt", "w") as f:
            f.write("{}\n".format("T" if self.face_id_var.get() else "F"))
            f.write(f"{self.new_item_combobox.get()}")

        messagebox.showinfo("Settings", "Successfully applied changes.")


    def show(self):
        self.sp_frame.pack(fill="both", expand=True)


    def hide(self):
        self.sp_frame.pack_forget()

    

class Main_Window():
    def __init__(self, root):
        self.root = root
        self.root.title("My Data Guard")
        self.root.geometry("800x600")

        # Sidebar (Left panel with buttons)
        self.sidebar = tk.Frame(self.root, bg="#2d3e50", width=120)
        self.sidebar.pack(side="left", fill="y")

        # Main content area (Right panel)
        self.content_area = tk.Frame(self.root)
        self.content_area.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.home_button = tk.Button(self.sidebar, text="Home", fg="white", font=("Arial", 10, "bold"), bg="#2d3e50", bd=0, padx=28, pady=20, command=self.show_home_page)
        self.home_button.pack()
        self.home_button.bind("<Enter>", lambda event: self.home_button.config(bg="#496481"))
        self.home_button.bind("<Leave>", lambda event: self.home_button.config(bg="#2d3e50"))

        self.settings_button = tk.Button(self.sidebar, text="Settings", fg="white", font=("Arial", 10, "bold"), bg="#2d3e50", bd=0, padx=22, pady=20, command=self.show_settings_page)
        self.settings_button.pack()
        self.settings_button.bind("<Enter>", lambda event: self.settings_button.config(bg="#496481"))
        self.settings_button.bind("<Leave>", lambda event: self.settings_button.config(bg="#2d3e50"))

        self.home_page = Home_Page(self.content_area)
        self.settings_page = Settings_Page(self.content_area)

        # Show Home Page by default
        self.show_home_page()

        # Bind the save_state method to the window close event
        root.protocol("WM_DELETE_WINDOW", self.on_closing)


    def show_home_page(self):
        self.settings_page.hide()
        self.home_page.show()

    
    def show_settings_page(self):
        self.home_page.hide()
        self.settings_page.show()

    
    def on_closing(self):
        self.home_page.save_state()
        self.root.destroy()