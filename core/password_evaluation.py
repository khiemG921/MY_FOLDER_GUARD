import random
import string

# Set password policy
policy = {
    'length': 8,          # Minimum password length is 8 characters
    'lowercase': 1,       # At least 1 lowercase letter
    'uppercase': 1,       # At least 1 uppercase letter
    'numbers': 1,         # At least 1 digit
    'special': 1          # At least 1 special character
}

def generate_password():
    # Determine a random length for the password (minimum length is the 'length' value from the policy)
    length = random.randint(policy['length'], 12)
    
    # Ensure the password contains at least the required number of characters from each category
    num_uppercase = random.randint(policy['uppercase'], length // 4)
    num_numbers = random.randint(policy['numbers'], length // 4)
    num_special = random.randint(policy['special'], length // 4)
    
    # Calculate the remaining characters to be filled with lowercase letters
    num_lowercase = length - (num_uppercase + num_numbers + num_special)
    
    # Character sets
    uppercases = string.ascii_uppercase
    lowercases = string.ascii_lowercase
    digits = string.digits
    specials = string.punctuation
    
    # Generate password components
    password = [
        random.choice(uppercases) for _ in range(num_uppercase)
    ] + [
        random.choice(digits) for _ in range(num_numbers)
    ] + [
        random.choice(specials) for _ in range(num_special)
    ] + [
        random.choice(lowercases) for _ in range(num_lowercase)
    ]
    
    # Shuffle the password to randomize the order of characters
    random.shuffle(password)
    
    return ''.join(password)

def evaluate_password(password):
    # Check the length of the password
    if len(password) < policy['length']:
        return False, generate_password()
    
    # Check the number of lowercase letters
    if sum(1 for c in password if c.islower()) < policy['lowercase']:
        return False, generate_password()
    
    # Check the number of uppercase letters
    if sum(1 for c in password if c.isupper()) < policy['uppercase']:
        return False, generate_password()
    
    # Check the number of digits
    if sum(1 for c in password if c.isdigit()) < policy['numbers']:
        return False, generate_password()
    
    # Check the number of special characters
    if sum(1 for c in password if c in string.punctuation) < policy['special']:
        return False, generate_password()
    
    return True, "Good password."