"""
Unit and integration tests for authentication, PBKDF2 hashing, and user registration.
"""

import unittest
import tempfile
import os
from auth import (
    hash_password, verify_password, validate_email,
    validate_password_strength, register_user, authenticate_user, bootstrap_admin
)
from database import init_db, get_connection

class TestAuthentication(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.db_path = self.temp_db.name
        self.temp_db.close()
        init_db(self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_password_hashing_and_verification(self):
        pwd = "SecurePassword123!"
        hashed = hash_password(pwd)
        self.assertNotEqual(pwd, hashed)
        self.assertTrue(verify_password(hashed, pwd))
        self.assertFalse(verify_password(hashed, "WrongPassword"))

    def test_password_strength_validation(self):
        valid, _ = validate_password_strength("StrongPass1!")
        self.assertTrue(valid)

        short, msg = validate_password_strength("Short1")
        self.assertFalse(short)
        self.assertIn("at least 8", msg)

        no_digit, _ = validate_password_strength("NoDigitsHere!")
        self.assertFalse(no_digit)

    def test_email_validation(self):
        self.assertTrue(validate_email("user@example.com"))
        self.assertTrue(validate_email("john.doe+work@domain.co.uk"))
        self.assertFalse(validate_email("notanemail"))
        self.assertFalse(validate_email("@missinguser.com"))

    def test_user_registration_success(self):
        ok, msg, user = register_user(
            email="candidate@test.com",
            password="CandidatePass123",
            full_name="Alex Smith",
            role="job_seeker",
            db_path=self.db_path
        )
        self.assertTrue(ok)
        self.assertEqual(user["email"], "candidate@test.com")
        self.assertEqual(user["role"], "job_seeker")

    def test_duplicate_email_prevention(self):
        register_user("alex@test.com", "Password123", "Alex One", "job_seeker", self.db_path)
        ok, msg, user = register_user("alex@test.com", "Password123", "Alex Two", "job_seeker", self.db_path)
        self.assertFalse(ok)
        self.assertIn("already exists", msg)
        self.assertIsNone(user)

    def test_authentication_success_and_failure(self):
        register_user("alex@test.com", "Password123", "Alex One", "job_seeker", self.db_path)
        ok, msg, user = authenticate_user("alex@test.com", "Password123", self.db_path)
        self.assertTrue(ok)
        self.assertEqual(user["full_name"], "Alex One")

        fail_ok, fail_msg, _ = authenticate_user("alex@test.com", "BadPass123", self.db_path)
        self.assertFalse(fail_ok)
        self.assertIn("Invalid", fail_msg)

    def test_admin_bootstrap(self):
        ok, msg = bootstrap_admin(self.db_path)
        self.assertTrue(ok)

        # Second bootstrap should recognize admin already exists
        ok2, msg2 = bootstrap_admin(self.db_path)
        self.assertFalse(ok2)
        self.assertIn("already exists", msg2)

if __name__ == "__main__":
    unittest.main()
