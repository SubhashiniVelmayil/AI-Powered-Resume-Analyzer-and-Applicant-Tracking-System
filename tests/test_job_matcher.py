"""
Unit and integration tests for job recommendation ranking and learning path generation.
"""

import unittest
import tempfile
import os
from database import init_db
from services.job_matcher import get_job_recommendations
from tests.test_resume_parser import SAMPLE_RESUME_TEXT

class TestJobMatcher(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.db_path = self.temp_db.name
        self.temp_db.close()
        init_db(self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_job_recommendations_ranking(self):
        recs = get_job_recommendations(SAMPLE_RESUME_TEXT, db_path=self.db_path)
        self.assertGreater(len(recs), 0)

        # Check descending sort by score
        scores = [r["match_score"] for r in recs]
        self.assertEqual(scores, sorted(scores, reverse=True))

        # First match should be Full Stack or Frontend because sample resume is strong in React/Python/TS
        top_match = recs[0]
        self.assertIn("Developer", top_match["title"])
        self.assertTrue(top_match["is_demo"])
        self.assertGreater(len(top_match["matched_skills"]), 0)
        self.assertGreater(len(top_match["suggested_learning_path"]), 0)

if __name__ == "__main__":
    unittest.main()
