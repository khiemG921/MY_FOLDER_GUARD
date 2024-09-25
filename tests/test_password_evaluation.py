import unittest
import string
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.password_evaluation import generate_password, evaluate_password

class TestPasswordFunctions(unittest.TestCase):

    def test_generate_password(self):
        password = generate_password()

        self.assertGreaterEqual(len(password), 8)
        self.assertLessEqual(len(password), 12)

        lowercase_count = sum(1 for c in password if c.islower())
        self.assertGreaterEqual(lowercase_count, 1)

        uppercase_count = sum(1 for c in password if c.isupper())
        self.assertGreaterEqual(uppercase_count, 1)

        number_count = sum(1 for c in password if c.isdigit())
        self.assertGreaterEqual(number_count, 1)

        special_count = sum(1 for c in password if c in string.punctuation)
        self.assertGreaterEqual(special_count, 1)

    def test_evaluate_password_valid(self):
        password = "A1b#abcd"
        is_valid, message = evaluate_password(password)
        self.assertTrue(is_valid)
        self.assertEqual(message, "Good password.")

    def test_evaluate_password_invalid_length(self):
        password = "A1b#"
        is_valid, generated_password = evaluate_password(password)
        self.assertFalse(is_valid)
        self.assertGreaterEqual(len(generated_password), 8)

    def test_evaluate_password_invalid_lowercase(self):
        password = "A1#ABCD"
        is_valid, generated_password = evaluate_password(password)
        self.assertFalse(is_valid)
        self.assertGreaterEqual(sum(1 for c in generated_password if c.islower()), 1)

    def test_evaluate_password_invalid_uppercase(self):
        password = "1a#abcd"
        is_valid, generated_password = evaluate_password(password)
        self.assertFalse(is_valid)
        self.assertGreaterEqual(sum(1 for c in generated_password if c.isupper()), 1)

    def test_evaluate_password_invalid_numbers(self):
        password = "A#abcdE"
        is_valid, generated_password = evaluate_password(password)
        self.assertFalse(is_valid)
        self.assertGreaterEqual(sum(1 for c in generated_password if c.isdigit()), 1)

    def test_evaluate_password_invalid_special(self):
        password = "A1bcdEfg"
        is_valid, generated_password = evaluate_password(password)
        self.assertFalse(is_valid)
        self.assertGreaterEqual(sum(1 for c in generated_password if c in string.punctuation), 1)

if __name__ == "__main__":
    unittest.main()
