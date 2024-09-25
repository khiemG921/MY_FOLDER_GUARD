from core.encryption import *

METHODS = ['Unprotect', 'Hide', 'Lock', 'Read-Only', 'Encrypt', 'Fully Protect']

def unprotect(path):
    """
    Bỏ bảo vệ (cho phép truy cập, hiển thị, có thể chỉnh sửa và giải mã) cho cả file và folder.
    """
    os.system(f'icacls "{path}" /remove:d Everyone')    # Cho phép truy cập
    os.system(f'attrib -h -r "{path}"')                 # Hiển thị và cho phép chỉnh sửa
    decrypt(path)                                       # Giải mã dữ liệu


def hide(path):
    """
    Ẩn file hoặc folder.
    """
    os.system(f'attrib +h "{path}"')


def lock(path):
    """
    Khóa file hoặc folder.
    """
    os.system(f'icacls "{path}" /deny Everyone:(OI)(CI)F')


def read_only(path):
    """
    Đặt file hoặc folder thành chỉ đọc.
    """
    os.system(f'attrib +r "{path}"')

def encrypt(path):
    """
    Mã hóa file hoặc folder
    """
    key = create_key()
    
    if os.path.isdir(path):
        encrypt_folder(path, key)
    else:
        encrypt_file(path, key)


def decrypt(path):
    """
    Giải mã file hoặc folder
    """
    key = get_key()

    if os.path.isdir(path):
        decrypt_folder(path, key)
    else:
        decrypt_file(path, key)


def fully_protect(path):
    """
    Mã hóa, khóa và ẩn file hoặc folder.
    """
    encrypt(path)
    hide(path)
    lock(path)