"""
SQLite Database Layer for AI Resume Analyzer & Applicant Tracking System.
Uses parameterized queries, relational constraints, foreign keys, and safe initialization.
"""

import sqlite3
import json
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
import os

from config import DATABASE_PATH

def get_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    """Creates a database connection with foreign keys enabled and row factory."""
    path = db_path or DATABASE_PATH
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_path: Optional[str] = None) -> None:
    """Initializes tables and seeds demo job data if not already present."""
    with get_connection(db_path) as conn:
        cursor = conn.cursor()

        # 1. Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('job_seeker', 'admin')),
                full_name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # 2. Resumes table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS resumes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                filename TEXT NOT NULL,
                file_size_bytes INTEGER NOT NULL,
                raw_text TEXT NOT NULL,
                is_scanned_notice BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
        """)

        # 3. Resume analyses table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS resume_analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                resume_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                overall_score INTEGER NOT NULL,
                rubric_breakdown_json TEXT NOT NULL,
                extracted_info_json TEXT NOT NULL,
                strengths_json TEXT NOT NULL,
                weaknesses_json TEXT NOT NULL,
                suggestions_json TEXT NOT NULL,
                ats_checks_json TEXT NOT NULL,
                ai_provider TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (resume_id) REFERENCES resumes(id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
        """)

        # 4. Jobs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                company TEXT NOT NULL,
                location TEXT NOT NULL,
                work_mode TEXT NOT NULL CHECK(work_mode IN ('Remote', 'Hybrid', 'On-site')),
                experience_level TEXT NOT NULL,
                salary_range TEXT NOT NULL,
                required_skills TEXT NOT NULL,
                preferred_qualifications TEXT NOT NULL,
                description TEXT NOT NULL,
                application_url TEXT NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                is_demo BOOLEAN DEFAULT 1,
                created_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL
            );
        """)

        # 5. Applications table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                resume_id INTEGER,
                status TEXT NOT NULL DEFAULT 'Applied' CHECK(status IN ('Applied', 'Under Review', 'Shortlisted', 'Interview', 'Selected', 'Rejected')),
                ats_match_score INTEGER,
                cover_note TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (resume_id) REFERENCES resumes(id) ON DELETE SET NULL,
                UNIQUE (job_id, user_id)
            );
        """)

        # 6. Application Notes table (Admin Internal Only)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS application_notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                application_id INTEGER NOT NULL,
                author_id INTEGER NOT NULL,
                note TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (application_id) REFERENCES applications(id) ON DELETE CASCADE,
                FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE CASCADE
            );
        """)

        conn.commit()

        # Seed sample demo jobs if table is empty
        cursor.execute("SELECT COUNT(*) FROM jobs;")
        count = cursor.fetchone()[0]
        if count == 0:
            seed_demo_jobs(conn)

def seed_demo_jobs(conn: sqlite3.Connection) -> None:
    """Inserts realistic demo jobs clearly marked as DEMO DATA."""
    demo_jobs = [
        (
            "Junior Full Stack Developer",
            "NovaTech Solutions (DEMO DATA)",
            "Austin, TX",
            "Hybrid",
            "Entry Level (0-2 years)",
            "$70,000 - $85,000/yr",
            "Python, React, TypeScript, SQL, Git, REST APIs",
            "Bachelor's in Computer Science, Docker, Tailwind CSS, Fastify or Express",
            "Seeking an enthusiastic junior developer to build clean full-stack web applications, optimize relational databases, and collaborate with agile teams. [DEMO DATA - Example Listing]",
            "https://example.com/careers/demo-job-1",
            1,
            1
        ),
        (
            "AI / Machine Learning Engineer",
            "Cortex Intelligence Labs (DEMO DATA)",
            "San Francisco, CA",
            "Remote",
            "Mid Level (2-4 years)",
            "$120,000 - $145,000/yr",
            "Python, PyTorch, LLMs, LangChain, RAG, REST APIs, Vector DBs, SQL",
            "Master's or relevant experience in NLP, prompt engineering, Hugging Face, Groq API",
            "Join our core AI research and development team to build production RAG pipelines, fine-tune models, and deploy scalable inference engines. [DEMO DATA - Example Listing]",
            "https://example.com/careers/demo-job-2",
            1,
            1
        ),
        (
            "Frontend Engineer (React & TypeScript)",
            "Aura Cloud Systems (DEMO DATA)",
            "New York, NY",
            "Remote",
            "Mid Level (2-5 years)",
            "$95,000 - $125,000/yr",
            "React, TypeScript, Next.js, Tailwind CSS, Responsive Design, State Management, Jest",
            "Experience with design systems, WebSockets, performance profiling, CI/CD",
            "Create pixel-perfect, responsive web applications with state-of-the-art UI/UX patterns and accessible component design. [DEMO DATA - Example Listing]",
            "https://example.com/careers/demo-job-3",
            1,
            1
        ),
        (
            "Data Analyst / BI Specialist",
            "Apex Strategic Analytics (DEMO DATA)",
            "Chicago, IL",
            "On-site",
            "Entry to Mid Level (1-3 years)",
            "$68,000 - $82,000/yr",
            "SQL, Python, pandas, Tableau, Power BI, Excel, Data Cleaning, Statistics",
            "Demonstrated experience with exploratory data analysis, KPI dashboards, business presentations",
            "Translate messy operational and commercial datasets into compelling executive dashboards and actionable business insights. [DEMO DATA - Example Listing]",
            "https://example.com/careers/demo-job-4",
            1,
            1
        ),
        (
            "DevOps & Cloud Infrastructure Engineer",
            "StratusOps Global (DEMO DATA)",
            "Seattle, WA",
            "Hybrid",
            "Senior (4+ years)",
            "$130,000 - $160,000/yr",
            "Docker, Kubernetes, AWS, Linux, Terraform, CI/CD, Python, Bash, Monitoring",
            "CKA certification, experience with Prometheus, Grafana, SOC2 compliance",
            "Design resilient cloud infrastructure, automate deployment pipelines, and ensure 99.99% system availability for mission-critical apps. [DEMO DATA - Example Listing]",
            "https://example.com/careers/demo-job-5",
            1,
            1
        )
    ]
    cursor = conn.cursor()
    cursor.executemany("""
        INSERT INTO jobs (
            title, company, location, work_mode, experience_level,
            salary_range, required_skills, preferred_qualifications,
            description, application_url, is_active, is_demo
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, demo_jobs)
    conn.commit()
