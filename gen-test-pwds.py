from werkzeug.security import generate_password_hash
import secrets

if __name__ == '__main__':
    test_password = "password123"
    hashed_password = generate_password_hash(test_password, method='pbkdf2:sha256', salt_length=16)   
    print(hashed_password)

    
