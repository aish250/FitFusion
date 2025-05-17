import streamlit as st
import json
import os
from hashlib import sha256
from pathlib import Path
from datetime import datetime

# Create data directory if it doesn't exist
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

# Path to the users database file
USERS_DB = DATA_DIR / "users.json"

def init_users_db():
    """Initialize the users database if it doesn't exist"""
    if not USERS_DB.exists():
        with open(USERS_DB, 'w') as f:
            json.dump({}, f)

def load_users():
    """Load users from the database"""
    init_users_db()
    with open(USERS_DB, 'r') as f:
        return json.load(f)

def save_users(users):
    """Save users to the database"""
    with open(USERS_DB, 'w') as f:
        json.dump(users, f)

def hash_password(password):
    """Hash a password for storing"""
    return sha256(password.encode()).hexdigest()

def create_user(username, password, email):
    """Create a new user"""
    users = load_users()
    if username in users:
        return False, "Username already exists"
    
    users[username] = {
        "password": hash_password(password),
        "email": email,
        "created_at": str(datetime.now())
    }
    save_users(users)
    return True, "User created successfully"

def verify_user(username, password):
    """Verify user credentials"""
    users = load_users()
    if username not in users:
        return False, "User not found"
    
    if users[username]["password"] != hash_password(password):
        return False, "Incorrect password"
    
    return True, "Login successful"

def init_session_state():
    """Initialize session state variables"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = None

def login_user(username, password):
    """Log in a user"""
    success, message = verify_user(username, password)
    if success:
        st.session_state.logged_in = True
        st.session_state.username = username
    return success, message

def logout_user():
    """Log out a user"""
    st.session_state.logged_in = False
    st.session_state.username = None

def get_current_user():
    """Get the currently logged in user"""
    return st.session_state.username if st.session_state.logged_in else None 

def init_session_state():
    """Initialize all required session state variables"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'redirect_to_login' not in st.session_state:
        st.session_state.redirect_to_login = False
    if 'login_time' not in st.session_state:
        st.session_state.login_time = None

def check_authenticated():
    """Check if user is logged in"""
    init_session_state()  # Initialize first!
    if not st.session_state.logged_in:
        st.session_state.redirect_to_login = True
        st.warning("Please login to access this page")
        st.stop()