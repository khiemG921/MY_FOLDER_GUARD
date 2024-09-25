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
├── core/
│   ├── encryption.py        # Encryption and decryption functionalities
│   ├── login_window.py      # Handles user login and face recognition logic
│   └── password_evaluation.py # Validates password strength
├── facial_images/           # Stores user face images for face recognition
├── folder_table/            # Stores folder protection state
├── images/                  # UI-related images (e.g., icons)
├── key/                     # Stores encryption keys
├── settings/                # Configuration files
├── main.py                  # Entry point for the application
├── main_window.py           # Main UI logic
├── README.md                # Project documentation
└── requirements.txt         # List of project dependencies
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