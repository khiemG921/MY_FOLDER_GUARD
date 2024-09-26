import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

def encrypt_file(file_path, key):
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv

    # Read the file to be encrypted
    with open(file_path, 'rb') as f:
        plaintext = f.read()

    # Encrypt the file content and pad it to block size
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))

    # Save the encrypted content with IV to a new file
    with open(file_path + '.enc', 'wb') as f:
        f.write(iv + ciphertext)
    
    os.system(f'del "{file_path}"')  # Delete the original file


def encrypt_folder(folder_path, key):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            encrypt_file(file_path, key)


def decrypt_file(file_path, key):
    # Read the encrypted file content
    with open(file_path, 'rb') as f:
        iv = f.read(16)  # Read the IV (first 16 bytes)
        ciphertext = f.read()

    # Decrypt the content
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

    # Save the decrypted content, removing '.enc' from the file name
    with open(file_path[:-4], 'wb') as f:
        f.write(plaintext)

    os.system(f'del "{file_path}"')  # Delete the encrypted file


def decrypt_folder(folder_path, key):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.enc'):
                file_path = os.path.join(root, file)
                decrypt_file(file_path, key)


def create_key():
    key_file = './data/key/encryption_key.bin'
    key = get_random_bytes(32)

    if not os.path.exists(key_file):
        with open(key_file, 'wb') as f:
            f.write(key)
    else:
        key = get_key()
    
    return key


def get_key():
    key_file = './data/key/encryption_key.bin'
    with open(key_file, 'rb') as f:
        return f.read()