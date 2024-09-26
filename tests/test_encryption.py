import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.encryption import *

class TestEncryption(unittest.TestCase):

    def setUp(self):
        self.test_file = 'test.txt'
        self.test_folder = 'test_folder'
        self.key = create_key()

        # Create a test file
        with open(self.test_file, 'w') as f:
            f.write('This is a test file.')

        # Create a test folder with files
        os.makedirs(self.test_folder, exist_ok=True)
        with open(os.path.join(self.test_folder, 'test1.txt'), 'w') as f:
            f.write('This is test file 1 in the folder.')
        with open(os.path.join(self.test_folder, 'test2.txt'), 'w') as f:
            f.write('This is test file 2 in the folder.')

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists(self.test_file + '.enc'):
            os.remove(self.test_file + '.enc')

        if os.path.exists(self.test_folder):
            for root, dirs, files in os.walk(self.test_folder, topdown=False):
                for file in files:
                    os.remove(os.path.join(root, file))
                os.rmdir(root)

    def test_encrypt_decrypt_file(self):
        # Encrypt the test file
        encrypt_file(self.test_file, self.key)
        self.assertFalse(os.path.exists(self.test_file))  # Check that original file is deleted
        self.assertTrue(os.path.exists(self.test_file + '.enc'))  # Encrypted file exists

        # Decrypt the file
        decrypt_file(self.test_file + '.enc', self.key)
        self.assertTrue(os.path.exists(self.test_file))  # Check that decrypted file exists

        # Check if content matches original
        with open(self.test_file, 'r') as f:
            content = f.read()
        self.assertEqual(content, 'This is a test file.')

    def test_encrypt_decrypt_folder(self):
        # Encrypt the folder
        encrypt_folder(self.test_folder, self.key)
        self.assertFalse(os.path.exists(os.path.join(self.test_folder, 'test1.txt')))
        self.assertTrue(os.path.exists(os.path.join(self.test_folder, 'test1.txt.enc')))

        # Decrypt the folder
        decrypt_folder(self.test_folder, self.key)
        self.assertTrue(os.path.exists(os.path.join(self.test_folder, 'test1.txt')))
        self.assertFalse(os.path.exists(os.path.join(self.test_folder, 'test1.txt.enc')))

        # Check file content
        with open(os.path.join(self.test_folder, 'test1.txt'), 'r') as f:
            content = f.read()
        self.assertEqual(content, 'This is test file 1 in the folder.')

if __name__ == '__main__':
    unittest.main()