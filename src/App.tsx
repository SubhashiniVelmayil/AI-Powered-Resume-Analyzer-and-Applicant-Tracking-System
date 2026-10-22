import React, { useState } from 'react';
import { Sidebar } from './components/Sidebar';
import { Navbar } from './components/Navbar';
import { DashboardView } from './pages/DashboardView';
import { ResumeAnalyzerView } from './pages/ResumeAnalyzerView';
import { ATSCheckerView } from './pages/ATSCheckerView';
import { JobRecommendationsView } from './pages/JobRecommendationsView';
import { ApplicationsView } from './pages/ApplicationsView';
import { AdminDashboardView } from './pages/AdminDashboardView';
import { ProfileView } from './pages/ProfileView';
import { ProjectRunnerModal } from './pages/ProjectRunnerModal';

import { UserRole, Job, Application, ApplicationStatus } from './types';
import { INITIAL_DEMO_JOBS, INITIAL_APPLICATIONS, SAMPLE_RESUMES } from './data/mockDatabase';

export default function App() {
  const [currentTab, setCurrentTab] = useState<string>('dashboard');
  const [userRole, setUserRole] = useState<UserRole>('job_seeker');
  const [userName, setUserName] = useState<string>('Alex Morgan');
  const [isPythonModalOpen, setIsPythonModalOpen] = useState<boolean>(false);

  // Application and Job states
  const [jobs, setJobs] = useState<Job[]>(INITIAL_DEMO_JOBS);
  const [applications, setApplications] = useState<Application[]>(INITIAL_APPLICATIONS);
  const [currentResumeText, setCurrentResumeText] = useState<string>(SAMPLE_RESUMES[0].text);
  const [currentResumeFilename, setCurrentResumeFilename] = useState<string>(SAMPLE_RESUMES[0].filename);

  // Toggle candidate <-> admin role
  const handleToggleRole = () => {
    if (userRole === 'admin') {
      setUserRole('job_seeker');
      setUserName('Alex Morgan');
    } else {
      setUserRole('admin');
      setUserName('System Administrator');
    }
  };

  // Submit application
  const handleApply = (job: Job, matchScore: number) => {
    const newApp: Application = {
      id: Date.now(),
      jobId: job.id,
      userId: 2,
      resumeFilename: currentResumeFilename,
      status: 'Applied',
      atsMatchScore: matchScore,
      createdAt: new Date().toISOString().split('T')[0],
      jobTitle: job.title,
      company: job.company,
      candidateName: userName,
      candidateEmail: userRole === 'admin' ? 'admin@resumetracker.local' : 'alex.morgan@example.com',
      notes: []
    };

    setApplications([newApp, ...applications]);
    setCurrentTab('applications');
  };

  // Update application status
  const handleUpdateApplicationStatus = (appId: number, newStatus: ApplicationStatus) => {
    setApplications(prev =>
      prev.map(a => (a.id === appId ? { ...a, status: newStatus } : a))
    );
  };

  // Add internal recruiter note
  const handleAddApplicationNote = (appId: number, noteText: string) => {
    setApplications(prev =>
      prev.map(a => {
        if (a.id === appId) {
          const notes = a.notes || [];
          return {
            ...a,
            notes: [
              ...notes,
              {
                id: Date.now(),
                applicationId: appId,
                authorName: userName,
                note: noteText,
                createdAt: new Date().toISOString().replace('T', ' ').slice(0, 16)
              }
            ]
          };
        }
        return a;
      })
    );
  };

  // Create job
  const handleCreateJob = (newJobData: Omit<Job, 'id' | 'createdAt'>) => {
    const created: Job = {
      ...newJobData,
      id: Date.now(),
      createdAt: new Date().toISOString().split('T')[0]
    };
    setJobs([created, ...jobs]);
  };

  // Toggle job active
  const handleToggleJobActive = (jobId: number) => {
    setJobs(prev =>
      prev.map(j => (j.id === jobId ? { ...j, isActive: !j.isActive } : j))
    );
  };

  const getPageInfo = () => {
    switch (currentTab) {
      case 'dashboard':
        return {
          title: 'Home Dashboard',
          subtitle: 'System overview, KPI metric cards, and quick career actions'
        };
      case 'resume_analyzer':
        return {
          title: 'Resume Analyzer & Rubric Scoring',
          subtitle: 'PDF parsing, 100-point rubric breakdown, and ATS checklist'
        };
      case 'ats_checker':
        return {
          title: 'Job-Specific ATS Score Checker',
          subtitle: 'Compare resume against role descriptions and uncover keyword gaps'
        };
      case 'jobs':
        return {
          title: 'Smart Job Recommendations',
          subtitle: 'Curated roles dynamically ranked by compatibility score'
        };
      case 'applications':
        return {
          title: 'My Applications',
          subtitle: 'Monitor review stages and interview milestones'
        };
      case 'admin':
        return {
          title: 'Administrator Console',
          subtitle: 'Candidate pipeline, recruiter notes, and job management'
        };
      case 'profile':
        return {
          title: 'Profile and Settings',
          subtitle: 'Account preferences, security details, and API configuration'
        };
      default:
        return {
          title: 'AI Resume Analyzer & ATS',
          subtitle: 'Analyze smarter. Improve your resume. Discover better opportunities.'
        };
    }
  };

  const pageInfo = getPageInfo();

  return (
    <div className="flex min-h-screen bg-radial from-[#0d1117] via-[#14122b] to-[#0a0f1d] text-slate-100 font-sans selection:bg-cyan-500/30 selection:text-cyan-200">
      {/* Sidebar Navigation */}
      <Sidebar
        currentTab={currentTab}
        onSelectTab={setCurrentTab}
        userRole={userRole}
        userName={userName}
        onOpenPythonModal={() => setIsPythonModalOpen(true)}
        onLogout={() => {
          setUserRole('job_seeker');
          setUserName('Alex Morgan');
          setCurrentTab('dashboard');
        }}
      />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0">
        <Navbar
          title={pageInfo.title}
          subtitle={pageInfo.subtitle}
          userRole={userRole}
          onToggleRole={handleToggleRole}
          onOpenPythonModal={() => setIsPythonModalOpen(true)}
        />

        <main className="flex-1 p-4 md:p-8 max-w-7xl w-full mx-auto">
          {currentTab === 'dashboard' && (
            <DashboardView
              onNavigate={setCurrentTab}
              applications={applications}
              jobs={jobs}
              userName={userName}
            />
          )}

          {currentTab === 'resume_analyzer' && (
            <ResumeAnalyzerView
              onAnalyzedResume={(text, fname) => {
                setCurrentResumeText(text);
                setCurrentResumeFilename(fname);
              }}
            />
          )}

          {currentTab === 'ats_checker' && (
            <ATSCheckerView
              jobs={jobs}
              currentResumeText={currentResumeText}
            />
          )}

          {currentTab === 'jobs' && (
            <JobRecommendationsView
              jobs={jobs}
              currentResumeText={currentResumeText}
              applications={applications}
              onApply={handleApply}
            />
          )}

          {currentTab === 'applications' && (
            <ApplicationsView
              applications={applications}
              onNavigateToJobs={() => setCurrentTab('jobs')}
            />
          )}

          {currentTab === 'admin' && (
            <AdminDashboardView
              jobs={jobs}
              applications={applications}
              onUpdateApplicationStatus={handleUpdateApplicationStatus}
              onAddApplicationNote={handleAddApplicationNote}
              onCreateJob={handleCreateJob}
              onToggleJobActive={handleToggleJobActive}
            />
          )}

          {currentTab === 'profile' && (
            <ProfileView
              userRole={userRole}
              userName={userName}
              onToggleRole={handleToggleRole}
              onOpenPythonModal={() => setIsPythonModalOpen(true)}
            />
          )}
        </main>
      </div>

      {/* Python Suite & Verification Modal */}
      <ProjectRunnerModal
        isOpen={isPythonModalOpen}
        onClose={() => setIsPythonModalOpen(false)}
      />
    </div>
  );
}
