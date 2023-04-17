from login import valid_login, user_exists, add_user, encrypt_password, decrypt_password
import sqlite3

def test_valid_login():
    assert valid_login("Jared", "Jared12345") == True

def test_valid_login_null_inputs():
    assert valid_login("", "") == False
    assert valid_login("Jared", "") == False
    assert valid_login("", "Jared12345") == False

def test_valid_login_incorrect_username_or_password():
    assert valid_login("Jared", "wrongpassword") == False
    assert valid_login("wrongusername", "Jared12345") == False

def test_user_exists():
    assert user_exists("Jared") == True
    assert user_exists("nonexistentuser") == False

def test_add_user():
    add_user("newuser", "newpassword")
    assert user_exists("newuser") == True

    conn = sqlite3.connect('userinfo.db')
    cursor = conn.cursor()
    # clean up database
    cursor.execute("DELETE FROM users WHERE username='newuser'")
    conn.commit()

def test_encrypt_password_and_decrypt_password():
    password = "mypassword"
    encrypted_password = encrypt_password(password)
    assert password != encrypted_password
    decrypted_password = decrypt_password(encrypted_password)
    assert password == decrypted_password

def run_tests():
    test_functions = [test_valid_login, test_valid_login_null_inputs, 
                      test_valid_login_incorrect_username_or_password, 
                      test_user_exists, test_add_user, test_encrypt_password_and_decrypt_password]
    
    for test_func in test_functions:
        try:
            test_func()
            print(f"{test_func.__name__}: Passed")
        except AssertionError:
            print(f"{test_func.__name__}: Failed")
            
run_tests()
