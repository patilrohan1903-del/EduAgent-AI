import bcrypt
import database

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def signup_user(username, password, email):
    if database.get_user(username):
        return False, "Username already exists."
    
    hashed_pw = hash_password(password)
    database.create_user(username, email, hashed_pw)
    return True, "User created successfully."

def login_user(username, password):
    user = database.get_user(username)
    if not user:
        return False, "User not found."
    
    if check_password(password, user['password']):
        return True, "Login successful."
    return False, "Incorrect password."

def update_password(username, new_password):
    user = database.get_user(username)
    if not user:
        return False
        
def update_password(username, new_password):
    user = database.get_user(username)
    if not user:
        return False
        
    hashed = hash_password(new_password)
    return database.update_user_password(username, hashed)
