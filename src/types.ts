export type UserRole = 'job_seeker' | 'admin';

export interface User {
  id: number;
  email: string;
  fullName: string;
  role: UserRole;
  createdAt: string;
}

export interface RubricBreakdown {
  contentQuality: number; // Max 25
  skillsRelevance: number; // Max 20
  projectsExperience: number; // Max 20
  educationCertifications: number; // Max 10
  achievementsImpact: number; // Max 15
  readabilityStructure: number; // Max 10
  totalScore: number;
}

export interface ATSCheckItem {
  check: string;
  passed: boolean;
  severity: 'High' | 'Medium' | 'Low' | 'None';
  issue?: string | null;
  recommendation: string;
}

export interface ResumeAnalysisResult {
  candidateInfo: {
    candidateName: string;
    email: string | null;
    phone: string | null;
  };
  skills: {
    technicalSkills: string[];
    softSkills: string[];
  };
  sections: {
    hasEducation: boolean;
    hasExperience: boolean;
    hasProjects: boolean;
    hasSkills: boolean;
    hasCertifications: boolean;
    hasAchievements: boolean;
  };
  metrics: string[];
  overallScore: number;
  rubricBreakdown: RubricBreakdown;
  explanations: Record<string, string>;
  atsChecks: ATSCheckItem[];
  strengths: { title: string; detail: string }[];
  weaknesses: { title: string; detail: string }[];
  suggestions: { category: string; action: string; before: string; after: string }[];
  disclaimer: string;
  provider: string;
}

export interface Job {
  id: number;
  title: string;
  company: string;
  location: string;
  workMode: 'Remote' | 'Hybrid' | 'On-site';
  experienceLevel: string;
  salaryRange: string;
  requiredSkills: string;
  preferredQualifications: string;
  description: string;
  applicationUrl: string;
  isActive: boolean;
  isDemo: boolean;
  createdAt: string;
}

export type ApplicationStatus =
  | 'Applied'
  | 'Under Review'
  | 'Shortlisted'
  | 'Interview'
  | 'Selected'
  | 'Rejected';

export interface ApplicationNote {
  id: number;
  applicationId: number;
  authorName: string;
  note: string;
  createdAt: string;
}

export interface Application {
  id: number;
  jobId: number;
  userId: number;
  resumeFilename: string;
  status: ApplicationStatus;
  atsMatchScore: number;
  coverNote?: string;
  createdAt: string;
  jobTitle: string;
  company: string;
  candidateName: string;
  candidateEmail: string;
  notes?: ApplicationNote[];
}

export interface ATSScoreResult {
  overallMatchScore: number;
  scoreBreakdown: {
    requiredSkills: number; // Max 40
    experienceEvidence: number; // Max 25
    educationMatch: number; // Max 15
    keywordCoverage: number; // Max 15
    certificationsMatch: number; // Max 5
    totalMatchScore: number;
  };
  matchedSkills: string[];
  relatedSkills: string[];
  missingSkills: string[];
  recommendations: string[];
  disclaimer: string;
}
