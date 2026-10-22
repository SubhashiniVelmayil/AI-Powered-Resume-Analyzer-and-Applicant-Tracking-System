"""
Unit and integration tests for ATS compatibility score calculation,
exact keyword matching, related skill inference, and missing skill detection.
"""

import unittest
from services.ats_scorer import compare_resume_to_job
from tests.test_resume_parser import SAMPLE_RESUME_TEXT

class TestATSScorer(unittest.TestCase):
    def test_high_compatibility_match(self):
        job_title = "Full Stack Engineer"
        job_description = "We are seeking a Full Stack Engineer to develop modern cloud applications using React, TypeScript, Python, and PostgreSQL."
        required_skills = "Python, React, TypeScript, PostgreSQL, Docker"
        preferred = "AWS, CI/CD, Git"

        result = compare_resume_to_job(
            resume_text=SAMPLE_RESUME_TEXT,
            job_title=job_title,
            job_description=job_description,
            required_skills=required_skills,
            preferred_qualifications=preferred
        )

        score = result["overall_match_score"]
        self.assertGreaterEqual(score, 75)
        self.assertIn("Python", result["matched_skills"])
        self.assertIn("React", result["matched_skills"])
        self.assertIn("TypeScript", result["matched_skills"])
        self.assertEqual(len(result["missing_skills"]), 0)
        self.assertIn("Advisory", result["disclaimer"])

    def test_missing_skills_and_related_skills_detection(self):
        job_title = "DevOps & Cloud Specialist"
        job_description = "Manage Kubernetes clusters, Terraform infrastructure, and Ruby on Rails microservices."
        required_skills = "Kubernetes, Terraform, Ruby, Go, AWS"

        result = compare_resume_to_job(
            resume_text=SAMPLE_RESUME_TEXT,
            job_title=job_title,
            job_description=job_description,
            required_skills=required_skills
        )

        # Kubernetes should be caught as related to Docker
        self.assertIn("AWS", result["matched_skills"])
        self.assertIn("Terraform", result["missing_skills"])
        self.assertIn("Ruby", result["missing_skills"])
        self.assertTrue(any("Kubernetes" in r for r in result["related_skills"]))

    def test_ats_score_breakdown_rubric(self):
        result = compare_resume_to_job(
            resume_text=SAMPLE_RESUME_TEXT,
            job_title="Software Developer",
            job_description="Build web applications with SQL and Git.",
            required_skills="SQL, Git"
        )

        breakdown = result["score_breakdown"]
        self.assertIn("required_skills", breakdown)
        self.assertIn("experience_evidence", breakdown)
        self.assertIn("education_match", breakdown)
        self.assertIn("keyword_coverage", breakdown)
        self.assertIn("certifications_match", breakdown)
        self.assertIn("total_match_score", breakdown)
        self.assertEqual(breakdown["total_match_score"], result["overall_match_score"])

if __name__ == "__main__":
    unittest.main()
