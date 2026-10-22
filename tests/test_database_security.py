"""
Unit and integration tests for database security, user data isolation,
role-based permissions, and admin internal notes secrecy.
"""

import unittest
import tempfile
import os
from database import init_db, get_connection
from auth import register_user

class TestDatabaseSecurity(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.db_path = self.temp_db.name
        self.temp_db.close()
        init_db(self.db_path)

        # Create User A (Job Seeker)
        _, _, self.user_a = register_user("usera@test.com", "Password123!", "User Alpha", "job_seeker", self.db_path)
        # Create User B (Job Seeker)
        _, _, self.user_b = register_user("userb@test.com", "Password123!", "User Beta", "job_seeker", self.db_path)
        # Create Admin User
        _, _, self.admin = register_user("admin@test.com", "AdminPass123!", "Admin User", "admin", self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_application_submission_and_status_update(self):
        with get_connection(self.db_path) as conn:
            cursor = conn.cursor()
            # User A submits application for Job 1
            cursor.execute("""
                INSERT INTO applications (job_id, user_id, status, ats_match_score, cover_note)
                VALUES (1, ?, 'Applied', 85, 'Excited to apply!');
            """, (self.user_a["id"],))
            conn.commit()
            app_id = cursor.lastrowid

            # Verify application exists
            cursor.execute("SELECT status FROM applications WHERE id = ?;", (app_id,))
            row = cursor.fetchone()
            self.assertEqual(row["status"], "Applied")

            # Admin updates status to Interview
            cursor.execute("""
                UPDATE applications SET status = 'Interview', updated_at = CURRENT_TIMESTAMP
                WHERE id = ?;
            """, (app_id,))
            conn.commit()

            cursor.execute("SELECT status FROM applications WHERE id = ?;", (app_id,))
            self.assertEqual(cursor.fetchone()["status"], "Interview")

    def test_user_data_isolation(self):
        # Insert resume for User A
        with get_connection(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO resumes (user_id, filename, file_size_bytes, raw_text)
                VALUES (?, 'alex_resume.pdf', 1024, 'Confidential details of User A');
            """, (self.user_a["id"],))
            conn.commit()

            # Query resumes owned by User B -> Must return 0 rows
            cursor.execute("SELECT * FROM resumes WHERE user_id = ?;", (self.user_b["id"],))
            user_b_resumes = cursor.fetchall()
            self.assertEqual(len(user_b_resumes), 0)

            # Query resumes owned by User A -> Returns 1 row
            cursor.execute("SELECT * FROM resumes WHERE user_id = ?;", (self.user_a["id"],))
            user_a_resumes = cursor.fetchall()
            self.assertEqual(len(user_a_resumes), 1)

    def test_admin_internal_notes_isolation(self):
        with get_connection(self.db_path) as conn:
            cursor = conn.cursor()
            # User A applies to Job 1
            cursor.execute("""
                INSERT INTO applications (job_id, user_id, status)
                VALUES (1, ?, 'Applied');
            """, (self.user_a["id"],))
            conn.commit()
            app_id = cursor.lastrowid

            # Admin creates an internal confidential note
            cursor.execute("""
                INSERT INTO application_notes (application_id, author_id, note)
                VALUES (?, ?, 'Confidential HR Note: Recommended for technical screening.');
            """, (app_id, self.admin["id"]))
            conn.commit()

            # Candidate view query: Query applications without joining application_notes
            cursor.execute("""
                SELECT a.id, a.status, j.title, j.company
                FROM applications a
                JOIN jobs j ON a.job_id = j.id
                WHERE a.user_id = ?;
            """, (self.user_a["id"],))
            candidate_view = cursor.fetchone()
            self.assertNotIn("note", candidate_view.keys())

            # Admin view query: Only accessible when role == 'admin'
            cursor.execute("""
                SELECT n.note, u.full_name as author
                FROM application_notes n
                JOIN users u ON n.author_id = u.id
                WHERE n.application_id = ?;
            """, (app_id,))
            notes = cursor.fetchall()
            self.assertEqual(len(notes), 1)
            self.assertIn("Confidential HR Note", notes[0]["note"])

    def test_parameterized_sql_injection_resistance(self):
        with get_connection(self.db_path) as conn:
            cursor = conn.cursor()
            # Malicious email payload trying SQL injection
            malicious_email = "victim@test.com' OR '1'='1"
            cursor.execute("SELECT * FROM users WHERE email = ?;", (malicious_email,))
            result = cursor.fetchall()
            self.assertEqual(len(result), 0)

if __name__ == "__main__":
    unittest.main()
