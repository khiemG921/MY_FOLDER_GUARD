import random
import string

# Thiết lập chính sách mật khẩu
policy = {
    'length': 8,          # Mật khẩu tối thiểu 8 ký tự
    'lowercase': 1,       # Ít nhất 1 chữ thường
    'uppercase': 1,       # Ít nhất 1 chữ hoa
    'numbers': 1,         # Ít nhất 1 chữ số
    'special': 1          # Ít nhất 1 ký tự đặc biệt
}

def generate_password():
    # Xác định độ dài ngẫu nhiên cho mật khẩu (tối thiểu là giá trị 'length' từ policy)
    length = random.randint(policy['length'], 12)
    
    # Đảm bảo mật khẩu có ít nhất số ký tự yêu cầu từ mỗi loại
    num_uppercase = random.randint(policy['uppercase'], length//4)
    num_numbers = random.randint(policy['numbers'], length//4)
    num_special = random.randint(policy['special'], length//4)
    
    # Tính số ký tự còn lại để lấp đầy bằng chữ thường
    num_lowercase = length - (num_uppercase + num_numbers + num_special)
    
    # Các tập ký tự
    uppercases = string.ascii_uppercase
    lowercases = string.ascii_lowercase
    digits = string.digits
    specials = string.punctuation
    
    # Tạo các phần tử của mật khẩu
    password = [
        random.choice(uppercases) for _ in range(num_uppercase)
    ] + [
        random.choice(digits) for _ in range(num_numbers)
    ] + [
        random.choice(specials) for _ in range(num_special)
    ] + [
        random.choice(lowercases) for _ in range(num_lowercase)
    ]
    
    # Xáo trộn mật khẩu để ngẫu nhiên hóa
    random.shuffle(password)
    
    return ''.join(password)

def evaluate_password(password):
    # Kiểm tra độ dài
    if len(password) < policy['length']:
        return False, generate_password()
    
    # Kiểm tra số lượng chữ thường
    if sum(1 for c in password if c.islower()) < policy['lowercase']:
        return False, generate_password()
    
    # Kiểm tra số lượng chữ hoa
    if sum(1 for c in password if c.isupper()) < policy['uppercase']:
        return False, generate_password()
    
    # Kiểm tra số lượng chữ số
    if sum(1 for c in password if c.isdigit()) < policy['numbers']:
        return False, generate_password()
    
    # Kiểm tra số lượng ký tự đặc biệt
    if sum(1 for c in password if c in string.punctuation) < policy['special']:
        return False, generate_password()
    
    return True, "Good password."