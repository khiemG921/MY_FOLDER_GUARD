import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

def encrypt_file(file_path, key):
    """
    Mã hóa file.
    """
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv

    with open(file_path, 'rb') as f:
        plaintext = f.read()

    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))

    with open(file_path + '.enc', 'wb') as f:
        f.write(iv + ciphertext)
    
    os.system(f'del "{file_path}"')


def encrypt_folder(folder_path, key):
    """
    Mã hóa folder.
    """
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            encrypt_file(file_path, key)


def decrypt_file(file_path, key):
    """
    Giải mã file.
    """
    with open(file_path, 'rb') as f:
        iv = f.read(16)  # Đọc IV
        ciphertext = f.read()

    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

    with open(file_path[:-4], 'wb') as f:  # Lưu tệp giải mã
        f.write(plaintext)

    os.system(f'del "{file_path}"')


def decrypt_folder(folder_path, key):
    """
    Giải mã folder.
    """
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.enc'):
                file_path = os.path.join(root, file)
                decrypt_file(file_path, key)


def create_key():
    """
    Tạo khóa để mã hóa
    """
    key_file = './data/key/encryption_key.bin'
    key = get_random_bytes(32)

    # Tạo khóa và lưu vào file khi mã hóa
    if not os.path.exists(key_file):
        with open(key_file, 'wb') as f:
            f.write(key)
    else:
        key = get_key()
    
    return key


def get_key():
    """
    Lấy khóa để mã hóa
    """
    key_file = './data/key/encryption_key.bin'
    with open(key_file, 'rb') as f:
        return f.read()