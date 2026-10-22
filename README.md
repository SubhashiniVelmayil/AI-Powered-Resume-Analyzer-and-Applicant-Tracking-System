# AI-Powered Resume Analyzer and Applicant Tracking System

An end-to-end web application that enables job seekers to upload resumes, analyze skills, audit ATS formatting vulnerabilities, calculate transparent rubric scores, receive AI-enhanced bullet point revisions, discover targeted job recommendations with personalized learning paths, and track submitted applications. 

The platform also includes a full Applicant Tracking System (ATS) Recruiter Console with candidate pipeline management, status tracking, confidential recruiter notes, job creation, and CSV reporting.

---

## 🌟 Key Features

1. **AI Resume Analyzer & Rubric Scoring**
   - Upload PDF resumes with automated size/type validation (<5MB).
   - Scanned and image-only PDF detection with OCR recommendations.
   - Transparent 100-point rubric breakdown:
     - *Content Quality & Completeness* (25 pts)
     - *Skills Relevance & Evidence* (20 pts)
     - *Projects & Practical Experience* (20 pts)
     - *Education & Certifications* (10 pts)
     - *Achievements & Quantifiable Metrics* (15 pts)
     - *Readability, Tone & Structure* (10 pts)
   - Strengths, weaknesses, and ATS formatting check audit.
   - Downloadable Diagnostic Report in Markdown format.

2. **Job-Specific ATS Compatibility Checker**
   - Compare resume text directly against curated or custom job descriptions.
   - 100-point transparent ATS compatibility rubric.
   - Distinguishes exact skill matches from related skills (e.g., JavaScript ↔ TypeScript, Docker ↔ Kubernetes).
   - Identifies keyword gaps and provides strategic recommendations to improve alignment.
   - Downloadable ATS comparison report.

3. **AI-Powered Resume Bullet Point Rewriter**
   - Converts weak or passive bullet points into high-impact accomplishment bullets using the Google XYZ formula: *"Accomplished [X] as measured by [Y] by doing [Z]"*.
   - Never fabricates credentials, dates, or companies; automatically inserts `[insert verified metric]` placeholders when facts are missing.
   - Supports Groq Cloud LLM inference (e.g., `llama-3.3-70b-versatile`) with deterministic local NLP fallback.

4. **Job Recommendation Engine**
   - Ranks database job postings by resume skill and experience match score.
   - Explains match rationale and suggests personalized learning paths for missing skills.
   - Filter by work mode (Remote, Hybrid, On-site) and minimum match threshold.
   - In-app 1-click ATS application submission.
   - Demo jobs clearly labeled with `DEMO DATA` badges.

5. **Applicant Tracking System (ATS) & Recruiter Console**
   - Candidate application tracking across 6 lifecycle stages:
     `Applied` → `Under Review` → `Shortlisted` → `Interview` → `Selected` → `Rejected`
   - Recruiter candidate search and status updates.
   - Confidential internal recruiter notes (strictly isolated on the backend and hidden from candidates).
   - Job creation, editing, and activation/deactivation.
   - CSV export for applicant tracking records.

6. **Enterprise-Grade Security & Privacy**
   - PBKDF2-HMAC-SHA256 password hashing with unique 16-byte random salts and 100,000 rounds.
   - Role-Based Access Control (`job_seeker` and `admin`).
   - SQLite parameterized queries preventing SQL injection.
   - User data isolation (candidates cannot access or delete other users' data).

---

## 🛠️ Technology Stack

- **Frontend & App Framework**: Streamlit (with custom CSS/HTML glassmorphism design system)
- **Programming Language**: Python 3.10+
- **PDF Extraction**: `pdfplumber` with pure-Python stream fallback
- **Data Processing**: Python Standard Library / `pandas`
- **Database**: SQLite3 with foreign keys and parameterized statements
- **AI Integration**: Groq API (`llama-3.3-70b-versatile`) with deterministic local NLP fallback
- **Testing**: `pytest` and `unittest`
- **Version Control**: Git & GitHub

---

## 📁 Project Folder Structure

```
ai_resume_analyzer/
├── app.py                      # Main Streamlit application entry point
├── requirements.txt            # Python dependencies
├── README.md                   # Complete documentation and setup guide
├── .gitignore                  # Git ignore rules for secrets and temporary files
├── .env.example                # Example environment variable configuration
├── config.py                   # Central configuration, scoring weights & defaults
├── database.py                 # SQLite database layer, migrations, and demo seed data
├── auth.py                     # PBKDF2 hashing, registration, login & admin bootstrap
├── models.py                   # Data models and typed structures
├── styles.py                   # Custom glassmorphism CSS & design system
├── pages/
│   ├── dashboard.py            # Home Dashboard & overview metrics
│   ├── resume_analyzer.py      # Resume uploading, parsing, scoring & history
│   ├── ats_checker.py          # Job-specific ATS compatibility & gap audit
│   ├── job_recommendations.py  # Smart job matching & 1-click application
│   ├── applications.py         # Candidate application pipeline view
│   ├── admin_dashboard.py      # Recruiter console, pipeline & job management
│   └── profile.py              # User profile, session & API configuration
├── services/
│   ├── pdf_parser.py           # Multi-level PDF parsing & scanned detection
│   ├── resume_analyzer.py      # Section detection, ATS checks & rubric scoring
│   ├── ats_scorer.py           # 100-point ATS rubric & semantic matching
│   ├── job_matcher.py          # Job recommendation & learning path engine
│   ├── ai_service.py           # Groq API client with local rule-based fallback
│   └── report_generator.py     # Markdown and CSV report formatters
├── utils/
│   ├── validators.py           # Input, status & job payload validators
│   └── helpers.py              # Badges, color thresholds & serialization
├── tests/
│   ├── test_auth.py            # Hashing, registration & login tests
│   ├── test_resume_parser.py   # PDF validation, scanned detection & rubric tests
│   ├── test_ats_scorer.py      # ATS scoring rubric & semantic matching tests
│   ├── test_job_matcher.py     # Job recommendation ranking tests
│   └── test_database_security.py # RBAC, data isolation & SQL injection tests
└── data/
    └── .gitkeep                # SQLite database directory
```

---

## 💻 Windows Setup & Installation Instructions

Follow these step-by-step instructions in Windows PowerShell or Command Prompt.

### 1. Prerequisites
- Python 3.10, 3.11, or 3.12 installed ([python.org](https://www.python.org/downloads/))
- Ensure `"Add Python to PATH"` was checked during installation.
- Git installed ([git-scm.com](https://git-scm.com/))

### 2. Clone or Navigate to the Project
```powershell
cd C:\path\to\your\project\folder
```

### 3. Create and Activate Virtual Environment
```powershell
# Create virtual environment
python -m venv venv

# Activate on Windows PowerShell:
.\venv\Scripts\Activate.ps1

# (Or on Windows Command Prompt cmd.exe):
venv\Scripts\activate.bat
```

### 4. Install Dependencies
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Copy `.env.example` to `.env`:
```powershell
copy .env.example .env
```
Open `.env` in any text editor (Notepad, VS Code) to configure:
```env
# Optional: Set your Groq API key for cloud LLM features
GROQ_API_KEY=""
GROQ_MODEL="llama-3.3-70b-versatile"

# Optional: Custom database file location
DATABASE_PATH="data/resume_ats.db"

# Initial admin bootstrap credentials
ADMIN_EMAIL="admin@resumetracker.local"
ADMIN_PASSWORD="AdminSecure2026!"
```
*Note: If no Groq API key is provided, the application runs seamlessly using the built-in local fallback engine.*

### 6. Initialize Database and Admin Account
The database and demo jobs are automatically seeded on first launch. You can also run the initialization script directly:
```powershell
python -c "from database import init_db; from auth import bootstrap_admin; init_db(); bootstrap_admin(); print('Database initialized!')"
```

### 7. Run Automated Tests
Execute the comprehensive test suite (20 automated tests):
```powershell
# Using standard Python unittest:
python -m unittest discover -s tests -p "test_*.py" -v

# Or using pytest:
pytest tests/ -v
```

### 8. Launch the Streamlit Web Application
```powershell
streamlit run app.py
```
Streamlit will automatically open your default browser at:
`http://localhost:8501`

To stop the server at any time, press `Ctrl + C` in your terminal.

---

## 🔑 Default Administrator Login

When the application first boots, an administrator account is automatically provisioned:
- **Email**: `admin@resumetracker.local`
- **Password**: `AdminSecure2026!`

You can also register a standard **Job Seeker** account directly from the landing page.

---

## 🚀 GitHub Push Instructions

To push this project to a new GitHub repository:

```powershell
# 1. Initialize git repository
git init

# 2. Stage all files
git add .

# 3. Create initial commit
git commit -m "Initial commit: AI-Powered Resume Analyzer and ATS"

# 4. Rename default branch to main
git branch -M main

# 5. Link to your GitHub remote repository (replace with your repo URL)
git remote add origin https://github.com/YOUR_USERNAME/ai-resume-analyzer-ats.git

# 6. Push to GitHub
git push -u origin main
```

---

## 🔒 Privacy & Ethical AI Principles

- **No Data Fabrication**: The AI rewrite tool never hallucinates degrees, previous companies, or metrics. Missing metrics are flagged with `[insert verified metric]`.
- **Human in the Loop**: AI compatibility scores are advisory heuristics. Candidates are never automatically disqualified by an algorithm.
- **Strict Data Isolation**: Recruiter notes and candidate application data are enforced server-side. Candidates can only access their own submissions.
- **Local-First Processing**: You can run the entire system 100% offline without sending any data to external cloud APIs.

---

## ⚖️ Advisory Disclaimer

Resume scores and ATS compatibility ratings provided by this platform are advisory estimates based on transparent rubric heuristics, keyword frequency, and section completeness. Proprietary employer ATS software and human hiring committees use diverse private evaluation criteria.
