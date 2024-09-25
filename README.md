**My Folder Guard** is a security-focused Python application designed to manage, protect, and encrypt folders and files. It integrates facial recognition for authentication, password validation, and multiple folder protection methods like hiding, locking, read-only access, and encryption. The app provides a seamless way to guard personal or sensitive data with minimal user interaction.

## Features

- **Folder Protection Methods**:
  - **Unprotect**: Removes protection from folders and files.
  - **Hide**: Makes folders and files invisible to casual users.
  - **Lock**: Restricts access to folders, denying all permissions.
  - **Read-Only**: Restricts modification of files or folders.
  - **Encrypt**: Encrypts folders or files with a secure key.
  - **Fully Protect**: Combines encryption, hiding, and locking for complete security.
  
- **Face Recognition**:
  - Uses `DeepFace` and OpenCV to provide face recognition-based authentication.
  - Detects masked faces using a specialized mask detection model.

- **Password Strength Validation**:
  - Evaluates password strength based on length, inclusion of uppercase, lowercase, numbers, and special characters.
  
- **UI Interface**:
  - Simple user-friendly graphical interface built with `Tkinter`, supporting folder protection selection, face ID creation, and toggling protection modes.

## Project Structure

```plaintext
project_root/
│
├── core/                           # Core application logic
│   ├── encryption.py               # Encryption logic
│   ├── face_identification.py      # Face identification functionality
│   ├── folder_protection.py        # Folder protection functionality
│   ├── login_window.py             # Login window logic
│   ├── main_window.py              # Main window UI logic
│   ├── password_evaluation.py      # Password strength evaluation
│
├── data/                           # Application data (should avoid large files here)
│   ├── facial_images/              # Saved facial images
│   ├── folder_table/               # Folder protection table
│   ├── key/                        # Encryption keys
│   ├── settings/                   # App settings
│
├── assets/                         # Static files (images, icons, etc.)
│   ├── images/                     # App-specific images/icons
│
├── tests/                          # Unit and integration tests
│   ├── test_folder_protection.py   # Unit test for folder_protection.py
│   ├── test_password_evaluation.py # Unit test for face_recognition.py
│   ├── ...                         # More tests as needed
│
├── main.py                         # Entry point for the program
├── .gitignore                   
├── setup.py                        # Setup script for packaging the app
└── README.md                       # Documentation about the project
```

## Usage

- Run the application by executing the main script:
  ```bash
  python main.py
  ```

- Use the `Main_Window` to:
  - Add folders to the protection list.
  - Select protection methods such as hide, lock, encrypt, etc.
  - Use facial recognition or password authentication to secure folders.

## Dependencies

- Python 3.7+
- OpenCV
- DeepFace
- Tkinter
- Pillow
- PyCryptodome