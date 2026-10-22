import React from 'react';
import { 
  FileText, 
  Target, 
  Briefcase, 
  Send, 
  ArrowRight, 
  Sparkles, 
  CheckCircle2, 
  Clock, 
  TrendingUp, 
  Database 
} from 'lucide-react';
import { Application, Job } from '../types';

interface DashboardViewProps {
  onNavigate: (tab: string) => void;
  applications: Application[];
  jobs: Job[];
  userName: string;
}

export const DashboardView: React.FC<DashboardViewProps> = ({
  onNavigate,
  applications,
  jobs,
  userName
}) => {
  const activeJobsCount = jobs.filter(j => j.isActive).length;
  const latestScore = applications.length > 0 ? `${applications[0].atsMatchScore}%` : '88%';

  return (
    <div className="space-y-6">
      {/* Welcome Banner */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-purple-950/60 via-[#161233] to-[#0a1829] border border-purple-500/20 p-6 md:p-8">
        <div className="relative z-10 max-w-2xl">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-300 text-xs font-semibold mb-3">
            <Sparkles className="w-3.5 h-3.5" />
            <span>AI Resume Intelligence & Applicant Tracking System</span>
          </div>
          <h1 className="text-2xl md:text-3xl font-extrabold text-white tracking-tight">
            Welcome back, <span className="bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">{userName}</span>
          </h1>
          <p className="text-slate-300 text-sm mt-2 leading-relaxed">
            Audit your resume with a transparent 100-point rubric, calculate job-specific ATS alignment, rewrite weak bullet points using the Google XYZ formula, and monitor applications in real-time.
          </p>
          <div className="flex flex-wrap items-center gap-3 mt-5">
            <button
              onClick={() => onNavigate('resume_analyzer')}
              className="flex items-center gap-2 px-4 py-2 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white text-xs font-bold shadow-lg shadow-cyan-500/25 transition-all transform hover:-translate-y-0.5"
            >
              <FileText className="w-4 h-4" />
              <span>Analyze a Resume</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={() => onNavigate('ats_checker')}
              className="flex items-center gap-2 px-4 py-2 rounded-xl bg-purple-900/40 hover:bg-purple-800/50 border border-purple-500/30 text-purple-200 text-xs font-semibold transition-colors"
            >
              <Target className="w-4 h-4 text-purple-400" />
              <span>Check ATS Score</span>
            </button>
          </div>
        </div>
        <div className="absolute right-0 top-0 bottom-0 w-1/3 bg-radial from-cyan-500/10 via-purple-600/10 to-transparent pointer-events-none" />
      </div>

      {/* KPI Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="rounded-xl bg-[#11162a]/70 border border-purple-900/30 p-5 hover:border-cyan-500/40 transition-all">
          <div className="flex items-center justify-between text-slate-400 text-xs font-semibold uppercase tracking-wider mb-2">
            <span>Analyzed Resumes</span>
            <FileText className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-2xl font-black text-white">3</div>
          <div className="text-[11px] text-cyan-400/80 mt-1 flex items-center gap-1">
            <TrendingUp className="w-3 h-3" />
            <span>Full rubric breakdowns stored</span>
          </div>
        </div>

        <div className="rounded-xl bg-[#11162a]/70 border border-purple-900/30 p-5 hover:border-purple-500/40 transition-all">
          <div className="flex items-center justify-between text-slate-400 text-xs font-semibold uppercase tracking-wider mb-2">
            <span>Latest Resume Score</span>
            <Target className="w-4 h-4 text-purple-400" />
          </div>
          <div className="text-2xl font-black text-white">{latestScore}</div>
          <div className="text-[11px] text-purple-300 mt-1">
            <span>Transparent 100-pt rubric</span>
          </div>
        </div>

        <div className="rounded-xl bg-[#11162a]/70 border border-purple-900/30 p-5 hover:border-emerald-500/40 transition-all">
          <div className="flex items-center justify-between text-slate-400 text-xs font-semibold uppercase tracking-wider mb-2">
            <span>Curated Job Listings</span>
            <Briefcase className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-black text-white">{activeJobsCount}</div>
          <div className="text-[11px] text-emerald-300 mt-1">
            <span>Active DEMO & partner roles</span>
          </div>
        </div>

        <div className="rounded-xl bg-[#11162a]/70 border border-purple-900/30 p-5 hover:border-blue-500/40 transition-all">
          <div className="flex items-center justify-between text-slate-400 text-xs font-semibold uppercase tracking-wider mb-2">
            <span>My Applications</span>
            <Send className="w-4 h-4 text-blue-400" />
          </div>
          <div className="text-2xl font-black text-white">{applications.length}</div>
          <div className="text-[11px] text-blue-300 mt-1">
            <span>Active recruitment pipeline</span>
          </div>
        </div>
      </div>

      {/* Quick Feature Navigation Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        <div 
          onClick={() => onNavigate('resume_analyzer')}
          className="group cursor-pointer rounded-2xl bg-gradient-to-b from-[#131936]/80 to-[#0d1226]/80 border border-purple-900/30 hover:border-cyan-500/50 p-6 transition-all duration-300 hover:shadow-xl hover:shadow-cyan-500/10 flex flex-col justify-between"
        >
          <div>
            <div className="w-10 h-10 rounded-xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400 mb-4 group-hover:scale-105 transition-transform">
              <FileText className="w-5 h-5" />
            </div>
            <h3 className="text-base font-bold text-white group-hover:text-cyan-300 transition-colors">
              Resume Diagnostic & Rubric Audit
            </h3>
            <p className="text-xs text-slate-400 mt-2 leading-relaxed">
              Upload PDF resumes to extract technical competencies, pinpoint weak phrasing, and run automated ATS formatting audits.
            </p>
          </div>
          <div className="flex items-center gap-1.5 text-xs font-semibold text-cyan-400 mt-5">
            <span>Open Analyzer</span>
            <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
          </div>
        </div>

        <div 
          onClick={() => onNavigate('ats_checker')}
          className="group cursor-pointer rounded-2xl bg-gradient-to-b from-[#131936]/80 to-[#0d1226]/80 border border-purple-900/30 hover:border-purple-500/50 p-6 transition-all duration-300 hover:shadow-xl hover:shadow-purple-500/10 flex flex-col justify-between"
        >
          <div>
            <div className="w-10 h-10 rounded-xl bg-purple-500/10 border border-purple-500/30 flex items-center justify-center text-purple-400 mb-4 group-hover:scale-105 transition-transform">
              <Target className="w-5 h-5" />
            </div>
            <h3 className="text-base font-bold text-white group-hover:text-purple-300 transition-colors">
              Job-Specific ATS Score Checker
            </h3>
            <p className="text-xs text-slate-400 mt-2 leading-relaxed">
              Match your resume against any job description. Distinguish exact skill matches from related tools and uncover missing keywords.
            </p>
          </div>
          <div className="flex items-center gap-1.5 text-xs font-semibold text-purple-400 mt-5">
            <span>Check Compatibility</span>
            <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
          </div>
        </div>

        <div 
          onClick={() => onNavigate('jobs')}
          className="group cursor-pointer rounded-2xl bg-gradient-to-b from-[#131936]/80 to-[#0d1226]/80 border border-purple-900/30 hover:border-emerald-500/50 p-6 transition-all duration-300 hover:shadow-xl hover:shadow-emerald-500/10 flex flex-col justify-between"
        >
          <div>
            <div className="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400 mb-4 group-hover:scale-105 transition-transform">
              <Briefcase className="w-5 h-5" />
            </div>
            <h3 className="text-base font-bold text-white group-hover:text-emerald-300 transition-colors">
              Smart Job Recommendations
            </h3>
            <p className="text-xs text-slate-400 mt-2 leading-relaxed">
              View curated roles automatically ranked by compatibility score with step-by-step learning paths for missing skills.
            </p>
          </div>
          <div className="flex items-center gap-1.5 text-xs font-semibold text-emerald-400 mt-5">
            <span>Explore Jobs</span>
            <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
          </div>
        </div>
      </div>

      {/* Recent Applications Pipeline */}
      <div className="rounded-2xl bg-[#0f1429]/80 border border-purple-900/30 p-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-base font-bold text-white">Active Application Pipeline</h3>
            <p className="text-xs text-slate-400">Current status of your submitted roles</p>
          </div>
          <button
            onClick={() => onNavigate('applications')}
            className="text-xs font-semibold text-cyan-400 hover:text-cyan-300 flex items-center gap-1"
          >
            <span>View All Applications</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>

        {applications.length === 0 ? (
          <div className="text-center py-8 text-slate-400 text-xs">
            No applications submitted yet. Browse Job Recommendations to submit your first application.
          </div>
        ) : (
          <div className="space-y-3">
            {applications.map((app) => (
              <div 
                key={app.id}
                className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 p-4 rounded-xl bg-slate-900/50 border border-slate-800/80 hover:border-slate-700 transition-all"
              >
                <div>
                  <h4 className="text-sm font-semibold text-white">{app.jobTitle}</h4>
                  <p className="text-xs text-slate-400">{app.company} • Submitted {app.createdAt}</p>
                </div>
                <div className="flex items-center gap-4">
                  <div className="text-right">
                    <div className="text-xs text-slate-400">ATS Match</div>
                    <div className="text-sm font-bold text-cyan-400">{app.atsMatchScore}%</div>
                  </div>
                  <span className={`text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider ${
                    app.status === 'Interview'
                      ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40'
                      : app.status === 'Under Review'
                      ? 'bg-amber-500/20 text-amber-300 border border-amber-500/40'
                      : 'bg-blue-500/20 text-blue-300 border border-blue-500/40'
                  }`}>
                    {app.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* System Architecture Callout */}
      <div className="rounded-xl bg-purple-950/20 border border-purple-500/20 p-4 flex flex-col md:flex-row items-center justify-between gap-3 text-xs text-slate-300">
        <div className="flex items-center gap-2">
          <Database className="w-4 h-4 text-purple-400 shrink-0" />
          <span>
            <strong>Database & Architecture</strong>: SQLite3 relational storage with isolated user records, parameterized queries, and safe PBKDF2 password authentication.
          </span>
        </div>
        <div className="flex items-center gap-2 shrink-0">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
          <span className="text-emerald-400 font-medium">Local NLP Engine & Groq API Ready</span>
        </div>
      </div>
    </div>
  );
};
