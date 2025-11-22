"""
Authentication and session management module
"""
import streamlit as st
import hashlib
import sqlite3
import json
from datetime import datetime, timedelta
import os

class AuthManager:
    def __init__(self, db_path="user_data.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize SQLite database for user management"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                email TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        ''')
        
        # Create sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                session_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username, password, email=None):
        """Register a new user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if user already exists
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            if cursor.fetchone():
                return False, "Username already exists"
            
            # Hash password and insert user
            password_hash = self.hash_password(password)
            cursor.execute(
                "INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)",
                (username, password_hash, email)
            )
            
            conn.commit()
            conn.close()
            return True, "User registered successfully"
            
        except Exception as e:
            return False, f"Registration failed: {str(e)}"
    
    def authenticate_user(self, username, password):
        """Authenticate user login"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            password_hash = self.hash_password(password)
            cursor.execute(
                "SELECT id, username, email FROM users WHERE username = ? AND password_hash = ?",
                (username, password_hash)
            )
            
            user = cursor.fetchone()
            if user:
                # Update last login
                cursor.execute(
                    "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?",
                    (user[0],)
                )
                conn.commit()
                conn.close()
                return True, user
            else:
                conn.close()
                return False, "Invalid username or password"
                
        except Exception as e:
            return False, f"Authentication failed: {str(e)}"
    
    def save_session(self, user_id, session_data):
        """Save user session data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Convert session data to JSON
            session_json = json.dumps(session_data)
            
            cursor.execute(
                "INSERT INTO sessions (user_id, session_data) VALUES (?, ?)",
                (user_id, session_json)
            )
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error saving session: {e}")
            return False
    
    def load_session(self, user_id):
        """Load user session data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT session_data FROM sessions WHERE user_id = ? ORDER BY created_at DESC LIMIT 1",
                (user_id,)
            )
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return json.loads(result[0])
            return None
            
        except Exception as e:
            print(f"Error loading session: {e}")
            return None
    
    def get_user_sessions(self, user_id):
        """Get all sessions for a user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT id, session_data, created_at FROM sessions WHERE user_id = ? ORDER BY created_at DESC",
                (user_id,)
            )
            
            sessions = cursor.fetchall()
            conn.close()
            
            return sessions
            
        except Exception as e:
            print(f"Error getting sessions: {e}")
            return []
    
    def delete_session(self, session_id):
        """Delete a specific session"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error deleting session: {e}")
            return False

def login_page():
    """Display login page"""
    st.title("🔐 Login to AI Investment Advisor")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button("Login")
            
            if submit_button:
                auth_manager = AuthManager()
                success, result = auth_manager.authenticate_user(username, password)
                
                if success:
                    st.session_state['authenticated'] = True
                    st.session_state['user_id'] = result[0]
                    st.session_state['username'] = result[1]
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error(result)
        
        st.markdown("---")
        st.markdown("Don't have an account? Register below:")
        
        with st.form("register_form"):
            reg_username = st.text_input("New Username")
            reg_password = st.text_input("New Password", type="password")
            reg_email = st.text_input("Email (optional)")
            reg_submit = st.form_submit_button("Register")
            
            if reg_submit:
                auth_manager = AuthManager()
                success, message = auth_manager.register_user(reg_username, reg_password, reg_email)
                
                if success:
                    st.success(message)
                else:
                    st.error(message)

def logout():
    """Logout user"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()
