from core.encryption import *

METHODS = ['Unprotect', 'Hide', 'Lock', 'Read-Only', 'Encrypt', 'Fully Protect']

def unprotect(path):
    os.system(f'icacls "{path}" /remove:d Everyone')    # Allow access
    os.system(f'attrib -h -r "{path}"')                 # Make visible and editable
    decrypt(path)                                       # Decrypt the data


def hide(path):
    os.system(f'attrib +h "{path}"')


def lock(path):
    os.system(f'icacls "{path}" /deny Everyone:(OI)(CI)F')


def read_only(path):
    os.system(f'attrib +r "{path}"')


def encrypt(path):
    key = create_key()  # Generate or retrieve encryption key
    
    if os.path.isdir(path):
        encrypt_folder(path, key)  # Encrypt entire folder
    else:
        encrypt_file(path, key)    # Encrypt single file


def decrypt(path):
    key = get_key()  # Retrieve encryption key

    if os.path.isdir(path):
        decrypt_folder(path, key)  # Decrypt entire folder
    else:
        decrypt_file(path, key)    # Decrypt single file


def fully_protect(path):
    encrypt(path)  # Encrypt the file or folder
    hide(path)     # Hide the file or folder
    lock(path)     # Lock the file or folder, denying access
