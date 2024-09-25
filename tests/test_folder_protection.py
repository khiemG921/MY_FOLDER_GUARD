import unittest
from unittest.mock import patch, call
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.folder_protection import *

class TestFolderProtection(unittest.TestCase):

    @patch('core.folder_protection.os.system')
    @patch('core.folder_protection.decrypt')
    def test_unprotect(self, mock_decrypt, mock_system):
        path = 'test_folder'
        unprotect(path)
        
        # Kiểm tra các lệnh hệ thống đã được gọi đúng cách
        mock_system.assert_has_calls([
            call(f'icacls "{path}" /remove:d Everyone'),
            call(f'attrib -h -r "{path}"')
        ])
        # Kiểm tra hàm decrypt đã được gọi
        mock_decrypt.assert_called_once_with(path)

    @patch('core.folder_protection.os.system')
    def test_hide(self, mock_system):
        path = 'test_folder'
        hide(path)
        
        # Kiểm tra lệnh hệ thống ẩn folder/file đã được gọi
        mock_system.assert_called_once_with(f'attrib +h "{path}"')

    @patch('core.folder_protection.os.system')
    def test_lock(self, mock_system):
        path = 'test_folder'
        lock(path)
        
        # Kiểm tra lệnh hệ thống khóa folder/file đã được gọi
        mock_system.assert_called_once_with(f'icacls "{path}" /deny Everyone:(OI)(CI)F')

    @patch('core.folder_protection.os.system')
    def test_read_only(self, mock_system):
        path = 'test_folder'
        read_only(path)
        
        # Kiểm tra lệnh hệ thống chỉ đọc đã được gọi
        mock_system.assert_called_once_with(f'attrib +r "{path}"')

    @patch('core.folder_protection.encrypt_file')
    @patch('core.folder_protection.encrypt_folder')
    @patch('core.folder_protection.create_key')
    @patch('core.folder_protection.os.path.isdir')
    def test_encrypt(self, mock_isdir, mock_create_key, mock_encrypt_folder, mock_encrypt_file):
        path = 'test_folder'
        mock_create_key.return_value = 'test_key'
        
        # Test mã hóa folder
        mock_isdir.return_value = True
        encrypt(path)
        mock_encrypt_folder.assert_called_once_with(path, 'test_key')
        mock_encrypt_file.assert_not_called()
        
        # Test mã hóa file
        mock_isdir.return_value = False
        encrypt(path)
        mock_encrypt_file.assert_called_once_with(path, 'test_key')

    @patch('core.folder_protection.decrypt_file')
    @patch('core.folder_protection.decrypt_folder')
    @patch('core.folder_protection.get_key')
    @patch('core.folder_protection.os.path.isdir')
    def test_decrypt(self, mock_isdir, mock_get_key, mock_decrypt_folder, mock_decrypt_file):
        path = 'test_folder'
        mock_get_key.return_value = 'test_key'
        
        # Test giải mã folder
        mock_isdir.return_value = True
        decrypt(path)
        mock_decrypt_folder.assert_called_once_with(path, 'test_key')
        mock_decrypt_file.assert_not_called()
        
        # Test giải mã file
        mock_isdir.return_value = False
        decrypt(path)
        mock_decrypt_file.assert_called_once_with(path, 'test_key')

    @patch('core.folder_protection.hide')
    @patch('core.folder_protection.lock')
    @patch('core.folder_protection.encrypt')
    def test_fully_protect(self, mock_encrypt, mock_lock, mock_hide):
        path = 'test_folder'
        fully_protect(path)
        
        # Kiểm tra thứ tự gọi các hàm
        mock_encrypt.assert_called_once_with(path)
        mock_hide.assert_called_once_with(path)
        mock_lock.assert_called_once_with(path)

if __name__ == "__main__":
    unittest.main()
