import { Job, Application, User, ResumeAnalysisResult, ATSScoreResult, ATSCheckItem } from '../types';

export const INITIAL_DEMO_JOBS: Job[] = [
  {
    id: 1,
    title: 'Junior Full Stack Developer',
    company: 'NovaTech Solutions (DEMO DATA)',
    location: 'Austin, TX',
    workMode: 'Hybrid',
    experienceLevel: 'Entry Level (0-2 years)',
    salaryRange: '$70,000 - $85,000/yr',
    requiredSkills: 'Python, React, TypeScript, SQL, Git, REST APIs',
    preferredQualifications: "Bachelor's in Computer Science, Docker, Tailwind CSS, Express",
    description: 'Seeking an enthusiastic junior developer to build clean full-stack web applications, optimize relational databases, and collaborate with agile teams. [DEMO DATA - Example Listing]',
    applicationUrl: 'https://example.com/careers/demo-job-1',
    isActive: true,
    isDemo: true,
    createdAt: '2026-03-10'
  },
  {
    id: 2,
    title: 'AI / Machine Learning Engineer',
    company: 'Cortex Intelligence Labs (DEMO DATA)',
    location: 'San Francisco, CA',
    workMode: 'Remote',
    experienceLevel: 'Mid Level (2-4 years)',
    salaryRange: '$120,000 - $145,000/yr',
    requiredSkills: 'Python, PyTorch, LLMs, LangChain, RAG, REST APIs, Vector DBs, SQL',
    preferredQualifications: "Master's or relevant experience in NLP, prompt engineering, Hugging Face, Groq API",
    description: 'Join our core AI research and development team to build production RAG pipelines, fine-tune models, and deploy scalable inference engines. [DEMO DATA - Example Listing]',
    applicationUrl: 'https://example.com/careers/demo-job-2',
    isActive: true,
    isDemo: true,
    createdAt: '2026-03-12'
  },
  {
    id: 3,
    title: 'Frontend Engineer (React & TypeScript)',
    company: 'Aura Cloud Systems (DEMO DATA)',
    location: 'New York, NY',
    workMode: 'Remote',
    experienceLevel: 'Mid Level (2-5 years)',
    salaryRange: '$95,000 - $125,000/yr',
    requiredSkills: 'React, TypeScript, Next.js, Tailwind CSS, Responsive Design, State Management, Jest',
    preferredQualifications: 'Experience with design systems, WebSockets, performance profiling, CI/CD',
    description: 'Create pixel-perfect, responsive web applications with state-of-the-art UI/UX patterns and accessible component design. [DEMO DATA - Example Listing]',
    applicationUrl: 'https://example.com/careers/demo-job-3',
    isActive: true,
    isDemo: true,
    createdAt: '2026-03-14'
  },
  {
    id: 4,
    title: 'Data Analyst / BI Specialist',
    company: 'Apex Strategic Analytics (DEMO DATA)',
    location: 'Chicago, IL',
    workMode: 'On-site',
    experienceLevel: 'Entry to Mid Level (1-3 years)',
    salaryRange: '$68,000 - $82,000/yr',
    requiredSkills: 'SQL, Python, Pandas, Tableau, Power BI, Excel, Data Cleaning, Statistics',
    preferredQualifications: 'Demonstrated experience with exploratory data analysis, KPI dashboards, business presentations',
    description: 'Translate messy operational and commercial datasets into compelling executive dashboards and actionable business insights. [DEMO DATA - Example Listing]',
    applicationUrl: 'https://example.com/careers/demo-job-4',
    isActive: true,
    isDemo: true,
    createdAt: '2026-03-15'
  },
  {
    id: 5,
    title: 'DevOps & Cloud Infrastructure Engineer',
    company: 'StratusOps Global (DEMO DATA)',
    location: 'Seattle, WA',
    workMode: 'Hybrid',
    experienceLevel: 'Senior (4+ years)',
    salaryRange: '$130,000 - $160,000/yr',
    requiredSkills: 'Docker, Kubernetes, AWS, Linux, Terraform, CI/CD, Python, Bash, Monitoring',
    preferredQualifications: 'CKA certification, experience with Prometheus, Grafana, SOC2 compliance',
    description: 'Design resilient cloud infrastructure, automate deployment pipelines, and ensure 99.99% system availability for mission-critical apps. [DEMO DATA - Example Listing]',
    applicationUrl: 'https://example.com/careers/demo-job-5',
    isActive: true,
    isDemo: true,
    createdAt: '2026-03-18'
  }
];

export const SAMPLE_RESUMES = [
  {
    name: 'Alex Morgan - Full Stack Engineer (Strong Sample)',
    filename: 'Alex_Morgan_Resume.pdf',
    text: `Alex Morgan
Email: alex.morgan@example.com | Phone: (555) 234-5678 | San Francisco, CA
LinkedIn: linkedin.com/in/alexmorgan | GitHub: github.com/alexmorgan

PROFESSIONAL SUMMARY
Dedicated Full Stack Software Engineer with 3+ years of experience developing scalable web applications, RESTful microservices, and distributed cloud systems.

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

E-Commerce Storefront | React, TypeScript, Stripe
- Engineered secure checkout workflow handling 1,500+ monthly orders with 99.9% uptime.

EDUCATION
Bachelor of Science in Computer Science | University of California, Berkeley | 2021
GPA: 3.8 / 4.0

CERTIFICATIONS
- AWS Certified Solutions Architect - Associate`
  },
  {
    name: 'Jordan Lee - AI/ML Engineer (Advanced Sample)',
    filename: 'Jordan_Lee_Resume.pdf',
    text: `Jordan Lee
Email: jordan.lee@aimail.com | Phone: (555) 789-0123 | Seattle, WA
GitHub: github.com/jordanlee-ai

PROFESSIONAL SUMMARY
Machine Learning Engineer specializing in Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), and high-throughput vector search systems.

TECHNICAL SKILLS
Core AI: Python, PyTorch, LangChain, RAG, Vector DBs, Hugging Face, Transformers
Engineering: Docker, Kubernetes, AWS, REST APIs, SQL, FastAPI, Git, Linux

WORK EXPERIENCE
AI Engineer | Cortex Intelligence Labs | 2023 - Present
- Built and deployed production RAG inference pipeline reducing context hallucination by 38%.
- Scaled embedding search with Pinecone and FAISS across 10,000,000+ documents with sub-50ms latency.
- Fine-tuned open-source LLMs utilizing LoRA and QLoRA, cutting inference costs by $42,000 annually.

Machine Learning Researcher | DataVision Research | 2021 - 2023
- Trained computer vision and NLP models on multi-GPU clusters using PyTorch.
- Authored 2 conference papers on self-supervised representation learning.

PROJECTS
Autonomous Code Review Agent | Python, LangChain, Groq API
- Designed automated pull request review bot identifying security vulnerabilities with 94% precision.

EDUCATION
Master of Science in Artificial Intelligence | Stanford University | 2021
Bachelor of Science in Electrical & Computer Engineering | University of Washington | 2019

CERTIFICATIONS
- TensorFlow Developer Certificate`
  },
  {
    name: 'Sam Taylor - Junior Developer (Needs Improvement)',
    filename: 'Sam_Taylor_Resume.pdf',
    text: `Sam Taylor
Email: samtaylor@email.com
Contact: Austin, TX

OBJECTIVE
Looking for a coding job where I can use my computer skills.

SKILLS
HTML, CSS, JavaScript, some Python, SQL.

EXPERIENCE
Intern | Web Firm | 2023 - 2024
- Worked on websites for clients.
- Helped with CSS fixes and updating text.
- Did bug testing.

PROJECTS
To-Do List App
- Built a to-do list using JavaScript.

EDUCATION
Associate Degree in General Studies | Austin Community College | 2023`
  }
];

export const INITIAL_APPLICATIONS: Application[] = [
  {
    id: 1,
    jobId: 1,
    userId: 2,
    resumeFilename: 'Alex_Morgan_Resume.pdf',
    status: 'Interview',
    atsMatchScore: 88,
    createdAt: '2026-03-14',
    jobTitle: 'Junior Full Stack Developer',
    company: 'NovaTech Solutions (DEMO DATA)',
    candidateName: 'Alex Morgan',
    candidateEmail: 'alex.morgan@example.com',
    notes: [
      {
        id: 1,
        applicationId: 1,
        authorName: 'System Administrator',
        note: 'Strong portfolio projects and clear React/TypeScript foundation. Scheduled for technical round.',
        createdAt: '2026-03-15 14:20'
      }
    ]
  },
  {
    id: 2,
    jobId: 2,
    userId: 2,
    resumeFilename: 'Alex_Morgan_Resume.pdf',
    status: 'Under Review',
    atsMatchScore: 76,
    createdAt: '2026-03-16',
    jobTitle: 'AI / Machine Learning Engineer',
    company: 'Cortex Intelligence Labs (DEMO DATA)',
    candidateName: 'Alex Morgan',
    candidateEmail: 'alex.morgan@example.com',
    notes: []
  }
];

// Technical skills dictionary
const COMMON_TECH_SKILLS = [
  'Python', 'JavaScript', 'TypeScript', 'React', 'Node.js', 'Express', 'Next.js',
  'HTML', 'CSS', 'Tailwind CSS', 'SQL', 'PostgreSQL', 'MySQL', 'MongoDB', 'SQLite',
  'Redis', 'Docker', 'Kubernetes', 'AWS', 'Git', 'GitHub', 'CI/CD', 'Linux',
  'REST APIs', 'FastAPI', 'Pandas', 'NumPy', 'PyTorch', 'Tableau', 'Power BI'
];

const COMMON_SOFT_SKILLS = [
  'Leadership', 'Communication', 'Problem Solving', 'Teamwork', 'Collaboration',
  'Time Management', 'Critical Thinking', 'Adaptability', 'Agile', 'Scrum'
];

export function analyzeResumeClient(text: string): ResumeAnalysisResult {
  const lower = text.toLowerCase();
  const wordCount = text.split(/\s+/).filter(Boolean).length;

  // Extract contact
  const emailMatch = text.match(/[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+/);
  const email = emailMatch ? emailMatch[0] : null;

  const phoneMatch = text.match(/(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}/);
  const phone = phoneMatch ? phoneMatch[0].trim() : null;

  const lines = text.split('\n').map(l => l.trim()).filter(Boolean);
  let candidateName = 'Alex Morgan';
  if (lines.length > 0 && lines[0].split(' ').length <= 4 && !lines[0].toLowerCase().includes('resume')) {
    candidateName = lines[0];
  }

  // Skills
  const technicalSkills = COMMON_TECH_SKILLS.filter(s => {
    const regex = new RegExp(`(?<![a-zA-Z0-9])${s.toLowerCase()}(?![a-zA-Z0-9])`, 'i');
    return regex.test(lower);
  });

  const softSkills = COMMON_SOFT_SKILLS.filter(s => {
    const regex = new RegExp(`(?<![a-zA-Z0-9])${s.toLowerCase()}(?![a-zA-Z0-9])`, 'i');
    return regex.test(lower);
  });

  // Sections
  const hasEducation = /\b(education|degree|university|college|bachelor|master|b\.s|m\.s|phd|gpa)\b/i.test(lower);
  const hasExperience = /\b(experience|employment|work history|professional history|internship)\b/i.test(lower);
  const hasProjects = /\b(projects|personal projects|portfolio)\b/i.test(lower);
  const hasSkills = /\b(skills|technical skills|technologies)\b/i.test(lower);
  const hasCertifications = /\b(certifications?|credentials?|aws certified|certified)\b/i.test(lower);
  const hasAchievements = /\b(achievements|awards|honors|publications)\b/i.test(lower);

  // Metrics
  const metrics = Array.from(new Set(text.match(/(\b\d+%\b|\$\d+[\d,]*|\b\d+x\b|\b\d+\+?\s*(?:users|clients|requests|transactions|ms|seconds|hours)\b)/gi) || []));

  // Rubric calculation
  const cqRatio = Math.min(1.0, wordCount / 450);
  const hasContact = Boolean(email && phone);
  const contentQuality = Math.round(25 * (0.6 * cqRatio + (hasContact ? 0.4 : 0.1)));

  const skillsRatio = Math.min(1.0, (technicalSkills.length * 1.5 + softSkills.length) / 12);
  const skillsRelevance = Math.round(20 * (0.7 * skillsRatio + (hasSkills ? 0.3 : 0.0)));

  const peRatio = hasExperience && hasProjects ? 1.0 : (hasExperience || hasProjects ? 0.7 : 0.2);
  const projectsExperience = Math.round(20 * peRatio);

  const ecRatio = hasEducation && hasCertifications ? 1.0 : (hasEducation ? 0.8 : 0.2);
  const educationCertifications = Math.round(10 * ecRatio);

  const metricRatio = metrics.length >= 4 ? 1.0 : (metrics.length >= 2 ? 0.75 : (metrics.length === 1 ? 0.45 : 0.15));
  const achievementsImpact = Math.round(15 * metricRatio);

  const readabilityStructure = Math.round(10 * (wordCount >= 250 && wordCount <= 900 ? 0.95 : 0.5));

  const totalScore = Math.min(100, contentQuality + skillsRelevance + projectsExperience + educationCertifications + achievementsImpact + readabilityStructure);

  // ATS Checks
  const atsChecks: ATSCheckItem[] = [
    {
      check: 'Contact Details',
      passed: Boolean(email && phone),
      severity: email && phone ? 'None' : 'High',
      issue: email && phone ? null : 'Missing phone number or email address in header.',
      recommendation: 'Ensure your email, phone, LinkedIn, and location are prominent.'
    },
    {
      check: 'Dedicated Skills Section',
      passed: hasSkills,
      severity: hasSkills ? 'None' : 'High',
      issue: hasSkills ? null : 'No distinct Skills header detected.',
      recommendation: 'Group competencies into Technical Skills, Frameworks, and Tools.'
    },
    {
      check: 'Education Section',
      passed: hasEducation,
      severity: hasEducation ? 'None' : 'Medium',
      issue: hasEducation ? null : 'No standard Education section detected.',
      recommendation: 'List degree, major, university, and graduation year.'
    },
    {
      check: 'Measurable Metrics & Impact',
      passed: metrics.length >= 2,
      severity: metrics.length >= 2 ? 'None' : 'High',
      issue: metrics.length >= 2 ? null : `Only ${metrics.length} quantified metric(s) found.`,
      recommendation: 'Add percentages, latency reductions, user counts, and revenue impact.'
    },
    {
      check: 'Resume Length & Substance',
      passed: wordCount >= 200 && wordCount <= 1100,
      severity: wordCount >= 200 && wordCount <= 1100 ? 'None' : 'Medium',
      issue: wordCount < 200 ? 'Resume is too brief.' : (wordCount > 1100 ? 'Resume exceeds standard length.' : null),
      recommendation: 'Target 350-750 words for early to mid-career roles.'
    }
  ];

  // Strengths
  const strengths = [];
  if (technicalSkills.length >= 5) {
    strengths.push({
      title: 'Strong Technical Skill Coverage',
      detail: `Highlighted ${technicalSkills.length} in-demand technical competencies including ${technicalSkills.slice(0, 4).join(', ')}.`
    });
  }
  if (metrics.length >= 2) {
    strengths.push({
      title: 'Quantified Accomplishments',
      detail: `Identified ${metrics.length} tangible metrics (${metrics.slice(0, 3).join(', ')}), proving business and technical impact.`
    });
  }
  if (hasProjects) {
    strengths.push({
      title: 'Practical Project Portfolio',
      detail: 'Features real hands-on projects showing practical software engineering execution.'
    });
  }
  if (strengths.length === 0) {
    strengths.push({
      title: 'Baseline Foundation',
      detail: 'Provides basic background information ready for enhancement.'
    });
  }

  // Weaknesses
  const weaknesses = [];
  if (metrics.length < 2) {
    weaknesses.push({
      title: 'Limited Measurable Evidence',
      detail: 'Bullet points focus on routine duties rather than quantified outcomes and metrics.'
    });
  }
  if (!hasCertifications) {
    weaknesses.push({
      title: 'No Industry Certifications Listed',
      detail: 'Missing recognized cloud or vendor certifications (e.g., AWS, Azure, GCP, Docker).'
    });
  }
  if (!hasContact) {
    weaknesses.push({
      title: 'Incomplete Contact Information',
      detail: 'Phone or email is missing, creating high rejection risks in automated ATS systems.'
    });
  }
  if (softSkills.length < 2) {
    weaknesses.push({
      title: 'Sparse Collaboration Skills',
      detail: 'Few soft skills or agile team collaboration attributes identified.'
    });
  }

  // Suggestions
  const suggestions = [
    {
      category: 'Quantifying Impact',
      action: "Transform task lists into Google XYZ statements: 'Accomplished [X] as measured by [Y] by doing [Z]'.",
      before: 'Worked on database queries and backend code.',
      after: 'Refactored PostgreSQL queries and implemented Redis caching, reducing API latency by 45% [insert verified metric].'
    },
    {
      category: 'Keyword Specificity',
      action: 'Replace vague phrases with explicit target technical names.',
      before: 'Experience with modern web frameworks and databases.',
      after: 'Engineered web applications utilizing React 19, TypeScript, and PostgreSQL with automated CI/CD.'
    },
    {
      category: 'Project Documentation',
      action: 'Add GitHub repository links and deployment URLs to every project entry.',
      before: 'Made an e-commerce website.',
      after: 'Developed full-stack e-commerce SPA handling 1,500+ monthly orders with Stripe integration.'
    }
  ];

  return {
    candidateInfo: { candidateName, email, phone },
    skills: { technicalSkills, softSkills },
    sections: { hasEducation, hasExperience, hasProjects, hasSkills, hasCertifications, hasAchievements },
    metrics,
    overallScore: totalScore,
    rubricBreakdown: {
      contentQuality,
      skillsRelevance,
      projectsExperience,
      educationCertifications,
      achievementsImpact,
      readabilityStructure,
      totalScore
    },
    explanations: {
      contentQuality: `Evaluated word count (${wordCount} words) and ${hasContact ? 'complete contact details' : 'missing contact fields'}.`,
      skillsRelevance: `Found ${technicalSkills.length} technical skills and ${softSkills.length} soft skills.`,
      projectsExperience: hasExperience && hasProjects ? 'Both professional experience and project portfolio present.' : 'Add both projects and work history.',
      educationCertifications: hasCertifications ? 'Education and verified certifications listed.' : 'Education listed. Certifications will boost this score.',
      achievementsImpact: `Detected ${metrics.length} quantified metrics (percentages, numbers, latency).`,
      readabilityStructure: 'Clean layout and standard professional terminology.'
    },
    atsChecks,
    strengths,
    weaknesses,
    suggestions,
    disclaimer: 'Advisory Diagnostic Estimate: This score is calculated via transparent rubric heuristics. Proprietary ATS systems use varied internal ranking weights.',
    provider: 'Local Rule-Based NLP & Rubric Engine'
  };
}

const RELATED_SKILLS_ONTOLOGY: Record<string, string[]> = {
  python: ['django', 'flask', 'fastapi', 'pandas', 'numpy', 'pytorch'],
  javascript: ['typescript', 'react', 'node.js', 'vue', 'angular', 'next.js'],
  typescript: ['javascript', 'react', 'node.js', 'angular'],
  react: ['next.js', 'javascript', 'typescript', 'redux', 'vue'],
  sql: ['postgresql', 'mysql', 'sqlite', 'oracle', 'database'],
  postgresql: ['sql', 'mysql', 'sqlite', 'relational database'],
  docker: ['kubernetes', 'containers', 'ci/cd', 'devops'],
  kubernetes: ['docker', 'containers', 'helm', 'devops'],
  terraform: ['cloudformation', 'ansible', 'iac'],
  aws: ['cloud', 'azure', 'gcp', 'lambda', 's3', 'ec2'],
  'machine learning': ['deep learning', 'pytorch', 'tensorflow', 'scikit-learn', 'nlp', 'llm'],
  git: ['github', 'gitlab', 'version control'],
  'rest apis': ['graphql', 'api', 'microservices', 'fastapi', 'express']
};

export function compareResumeToJobClient(resumeText: string, jobTitle: string, jobDesc: string, requiredSkills: string): ATSScoreResult {
  const lower = resumeText.toLowerCase();
  const reqList = requiredSkills.split(/[,|/;\n]+/).map(s => s.trim()).filter(Boolean);

  const matchedSkills: string[] = [];
  const relatedSkills: string[] = [];
  const missingSkills: string[] = [];

  for (const skill of reqList) {
    const clean = skill.toLowerCase();
    const regex = new RegExp(`(?<![a-zA-Z0-9])${clean}(?![a-zA-Z0-9])`, 'i');
    if (regex.test(lower)) {
      matchedSkills.push(skill);
    } else {
      const relatives = RELATED_SKILLS_ONTOLOGY[clean] || [];
      const foundRel = relatives.find(r => new RegExp(`(?<![a-zA-Z0-9])${r}(?![a-zA-Z0-9])`, 'i').test(lower));
      if (foundRel) {
        relatedSkills.push(`${skill} (Evidenced via related skill: ${foundRel.toUpperCase()})`);
      } else {
        missingSkills.push(skill);
      }
    }
  }

  // Required skill coverage (40 pts)
  const coverageRatio = (matchedSkills.length * 1.0 + relatedSkills.length * 0.5) / Math.max(1, reqList.length);
  const requiredSkillsScore = Math.round(40 * Math.min(1.0, coverageRatio));

  // Experience & projects (25 pts)
  const titleWords = jobTitle.split(/\s+/).filter(w => w.length > 3).map(w => w.toLowerCase());
  const titleMatches = titleWords.filter(w => lower.includes(w));
  const hasProj = /\b(project|portfolio|built|developed)\b/i.test(lower);
  const expRatio = (titleMatches.length / Math.max(1, titleWords.length)) * 0.5 + (hasProj ? 0.5 : 0.2);
  const experienceEvidence = Math.round(25 * Math.min(1.0, expRatio));

  // Education (15 pts)
  const hasDegree = /\b(bachelor|master|b\.s|m\.s|degree|computer science)\b/i.test(lower);
  const educationMatch = hasDegree ? 14 : 7;

  // Keyword coverage (15 pts)
  const descWords = Array.from(new Set(jobDesc.toLowerCase().match(/\b[a-z]{4,}\b/g) || [])).slice(0, 20);
  const descMatches = descWords.filter(w => lower.includes(w));
  const keywordCoverage = Math.round(15 * Math.min(1.0, (descMatches.length / Math.max(1, descWords.length)) * 1.3));

  // Certifications (5 pts)
  const hasCert = /\b(certified|certification|aws|azure|gcp|docker)\b/i.test(lower);
  const certificationsMatch = hasCert ? 5 : 1;

  const totalMatchScore = Math.min(100, requiredSkillsScore + experienceEvidence + educationMatch + keywordCoverage + certificationsMatch);

  const recommendations = [];
  if (missingSkills.length > 0) {
    recommendations.push(`Incorporate missing required skills (${missingSkills.slice(0, 3).join(', ')}) into your projects if experienced.`);
  }
  if (relatedSkills.length > 0) {
    recommendations.push('Replace generic terms with exact target names: For example, mention TypeScript directly if requested rather than just JavaScript.');
  }
  if (keywordCoverage < 9) {
    recommendations.push('Mirror key architectural vocabulary from the job description in your technical summaries.');
  }

  return {
    overallMatchScore: totalMatchScore,
    scoreBreakdown: {
      requiredSkills: requiredSkillsScore,
      experienceEvidence,
      educationMatch,
      keywordCoverage,
      certificationsMatch,
      totalMatchScore
    },
    matchedSkills,
    relatedSkills,
    missingSkills,
    recommendations,
    disclaimer: 'Advisory Compatibility Estimate: This assessment is an analytical heuristic based on requirements and keyword coverage. Real-world ATS systems use diverse proprietary scoring algorithms.'
  };
}

export function rewriteBulletClient(bullet: string): { original: string; improved: string; verb: string } {
  const clean = bullet.trim().replace(/^[•\-\*]\s*/, '');
  if (!clean) {
    return { original: '', improved: '', verb: 'Engineered' };
  }

  const replacements: [RegExp, string][] = [
    [/worked on/i, 'Architected and delivered'],
    [/helped with/i, 'Collaborated cross-functionally to optimize'],
    [/was responsible for/i, 'Spearheaded end-to-end execution of'],
    [/made/i, 'Engineered and deployed'],
    [/fixed bugs/i, 'Diagnosed and resolved critical production defects, improving system stability by [insert verified %]'],
    [/managed/i, 'Orchestrated and scaled'],
    [/did testing/i, 'Authored comprehensive automated test suites achieving [insert verified %] code coverage'],
    [/learned/i, 'Rapidly acquired expertise in and applied']
  ];

  let improved = clean;
  for (const [pattern, rep] of replacements) {
    if (pattern.test(improved)) {
      improved = improved.replace(pattern, rep);
      break;
    }
  }

  if (improved === clean) {
    improved = `Engineered ${clean}, driving measurable performance gains of [insert verified metric].`;
  }

  const verb = improved.split(' ')[0] || 'Engineered';
  return { original: clean, improved, verb };
}
