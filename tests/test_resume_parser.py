"""
Unit and integration tests for PDF parsing, scanned resume detection, and resume scoring.
"""

import unittest
from services.pdf_parser import validate_pdf_file, extract_text_from_pdf
from services.resume_analyzer import analyze_resume_text, extract_skills, detect_sections

SAMPLE_RESUME_TEXT = """
Alex Morgan
Email: alex.morgan@example.com | Phone: (555) 234-5678 | San Francisco, CA
LinkedIn: linkedin.com/in/alexmorgan | GitHub: github.com/alexmorgan

SUMMARY
Dedicated Full Stack Software Engineer with 3+ years of experience building scalable web applications,
RESTful microservices, and distributed cloud systems.

TECHNICAL SKILLS
Languages: Python, TypeScript, JavaScript, SQL, HTML, CSS
Frameworks & Libraries: React, Node.js, Express, FastAPI, Tailwind CSS, Pandas
Databases & Cloud: PostgreSQL, SQLite, Redis, Docker, AWS, Git, CI/CD

PROFESSIONAL EXPERIENCE
Software Engineer | Apex Cloud Systems | 2023 - Present
- Architected and deployed microservices handling 250,000+ daily API requests using Python and FastAPI.
- Optimized database indexing and query patterns on PostgreSQL, reducing response latency by 45%.
- Built dynamic user interfaces in React and TypeScript, boosting client engagement by 28%.

Junior Developer | ByteCraft Interactive | 2021 - 2023
- Developed full-stack features with Node.js, Express, and React for 5,000+ active enterprise users.
- Automated testing workflows with Jest and GitHub Actions, achieving 92% code coverage.

PROJECTS
AI Resume Diagnostic Tool | Python, React, SQLite
- Created an intelligent resume analysis platform calculating ATS compatibility scores.
- Implemented responsive dark UI with glassmorphism styling and real-time rubric feedback.

EDUCATION
Bachelor of Science in Computer Science | University of California, Berkeley | 2021
GPA: 3.8 / 4.0

CERTIFICATIONS
- AWS Certified Solutions Architect - Associate
"""

class TestResumeParser(unittest.TestCase):
    def test_file_validation_rules(self):
        # Valid PDF extension and size
        valid, _ = validate_pdf_file("my_resume.pdf", 2048)
        self.assertTrue(valid)

        # Invalid extension
        invalid_ext, msg = validate_pdf_file("my_resume.docx", 2048)
        self.assertFalse(invalid_ext)
        self.assertIn("Invalid file type", msg)

        # Empty file
        empty_file, msg = validate_pdf_file("empty.pdf", 0)
        self.assertFalse(empty_file)
        self.assertIn("empty", msg)

        # Oversized file (> 5MB)
        oversized, msg = validate_pdf_file("huge.pdf", 6 * 1024 * 1024)
        self.assertFalse(oversized)
        self.assertIn("exceeds", msg)

    def test_scanned_pdf_detection(self):
        # Empty or tiny byte content simulates image-only PDF without OCR layer
        dummy_pdf_bytes = b"%PDF-1.4 ... binary image data with no font streams ..."
        result = extract_text_from_pdf(dummy_pdf_bytes, "scanned_doc.pdf")
        self.assertTrue(result["success"])
        self.assertTrue(result["is_scanned"])
        self.assertIn("Scanned or Image-Only PDF Detected", result["warning"])

    def test_skill_extraction(self):
        skills = extract_skills(SAMPLE_RESUME_TEXT)
        tech = skills["technical_skills"]
        self.assertIn("Python", tech)
        self.assertIn("React", tech)
        self.assertIn("PostgreSQL", tech)
        self.assertIn("Docker", tech)
        self.assertIn("TypeScript", tech)

    def test_section_detection(self):
        sections = detect_sections(SAMPLE_RESUME_TEXT)
        self.assertTrue(sections["has_education"])
        self.assertTrue(sections["has_experience"])
        self.assertTrue(sections["has_skills"])
        self.assertTrue(sections["has_projects"])
        self.assertTrue(sections["has_certifications"])

    def test_resume_analysis_score_and_rubric(self):
        analysis = analyze_resume_text(SAMPLE_RESUME_TEXT)
        score = analysis["overall_score"]
        self.assertGreaterEqual(score, 70)
        self.assertLessEqual(score, 100)

        # Verify rubric breakdown structure
        breakdown = analysis["rubric_breakdown"]
        self.assertIn("content_quality", breakdown)
        self.assertIn("skills_relevance", breakdown)
        self.assertIn("projects_experience", breakdown)
        self.assertIn("education_certifications", breakdown)
        self.assertIn("achievements_impact", breakdown)
        self.assertIn("readability_structure", breakdown)

        # Verify candidate info parsing
        cand = analysis["candidate_info"]
        self.assertEqual(cand["email"], "alex.morgan@example.com")
        self.assertEqual(cand["phone"], "(555) 234-5678")

if __name__ == "__main__":
    unittest.main()
