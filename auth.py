"""
Authentication and Authorization Module.
Provides secure PBKDF2 password hashing, salt generation, role-based checks,
and safe administrator bootstrap logic.
"""

import hashlib
import hmac
import os
import re
from typing import Optional, Dict, Any, Tuple
from database import get_connection
from config import ADMIN_DEFAULT_EMAIL, ADMIN_DEFAULT_PASSWORD

SALT_BYTES = 16
HASH_ITERATIONS = 100_000

def hash_password(password: str) -> str:
    """Hashes a password using PBKDF2-HMAC-SHA256 with a unique random salt."""
    salt = os.urandom(SALT_BYTES)
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        HASH_ITERATIONS
    )
    # Store salt and key in hex format: salt$hash
    return f"{salt.hex()}${key.hex()}"

def verify_password(stored_hash: str, provided_password: str) -> bool:
    """Verifies a password against the stored salt$hash string."""
    try:
        salt_hex, key_hex = stored_hash.split('$')
        salt = bytes.fromhex(salt_hex)
        expected_key = bytes.fromhex(key_hex)
        derived_key = hashlib.pbkdf2_hmac(
            'sha256',
            provided_password.encode('utf-8'),
            salt,
            HASH_ITERATIONS
        )
        return hmac.compare_digest(derived_key, expected_key)
    except Exception:
        return False

def validate_email(email: str) -> bool:
    """Validates email format using regex."""
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(pattern, email.strip()))

def validate_password_strength(password: str) -> Tuple[bool, str]:
    """Validates password strength (min 8 chars, mixed chars)."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter."
    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter."
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one digit."
    return True, "Password is valid."

def register_user(email: str, password: str, full_name: str, role: str = "job_seeker", db_path: Optional[str] = None) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """
    Registers a new user in the system.
    Prevents duplicate emails and validates inputs.
    """
    email = email.strip().lower()
    full_name = full_name.strip()

    if not full_name:
        return False, "Full name cannot be blank.", None

    if not validate_email(email):
        return False, "Please enter a valid email address.", None

    is_valid_pwd, pwd_msg = validate_password_strength(password)
    if not is_valid_pwd:
        return False, pwd_msg, None

    if role not in ("job_seeker", "admin"):
        return False, f"Invalid role: {role}", None

    pwd_hash = hash_password(password)

    try:
        with get_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE email = ?;", (email,))
            if cursor.fetchone():
                return False, "An account with this email address already exists.", None

            cursor.execute("""
                INSERT INTO users (email, password_hash, role, full_name)
                VALUES (?, ?, ?, ?);
            """, (email, pwd_hash, role, full_name))
            conn.commit()

            user_id = cursor.lastrowid
            user_data = {
                "id": user_id,
                "email": email,
                "full_name": full_name,
                "role": role
            }
            return True, "Account registered successfully.", user_data
    except Exception as e:
        return False, f"Database error during registration: {str(e)}", None

def authenticate_user(email: str, password: str, db_path: Optional[str] = None) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """Authenticates a user by email and password."""
    email = email.strip().lower()

    if not email or not password:
        return False, "Email and password are required.", None

    try:
        with get_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, email, password_hash, role, full_name FROM users WHERE email = ?;", (email,))
            row = cursor.fetchone()

            if not row:
                return False, "Invalid email or password.", None

            if not verify_password(row["password_hash"], password):
                return False, "Invalid email or password.", None

            user_dict = {
                "id": row["id"],
                "email": row["email"],
                "full_name": row["full_name"],
                "role": row["role"]
            }
            return True, "Login successful.", user_dict
    except Exception as e:
        return False, f"Authentication error: {str(e)}", None

def bootstrap_admin(db_path: Optional[str] = None) -> Tuple[bool, str]:
    """
    Safe first-run admin bootstrapper.
    Checks if an administrator exists. If none exists, creates one from config.
    """
    try:
        with get_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'admin';")
            count = cursor.fetchone()[0]
            if count == 0:
                pwd_hash = hash_password(ADMIN_DEFAULT_PASSWORD)
                cursor.execute("""
                    INSERT INTO users (email, password_hash, role, full_name)
                    VALUES (?, ?, 'admin', 'System Administrator');
                """, (ADMIN_DEFAULT_EMAIL.lower(), pwd_hash))
                conn.commit()
                return True, f"Admin account created for {ADMIN_DEFAULT_EMAIL}"
            return False, "Admin account already exists."
    except Exception as e:
        return False, f"Error creating admin account: {str(e)}"
