import React, { useState } from 'react';
import { 
  ShieldCheck, 
  Users, 
  FileText, 
  Briefcase, 
  Send, 
  Download, 
  Plus, 
  Search, 
  Lock, 
  MessageSquare,
  CheckCircle2,
  ToggleLeft,
  ToggleRight
} from 'lucide-react';
import { Job, Application, ApplicationStatus } from '../types';

interface AdminDashboardViewProps {
  jobs: Job[];
  applications: Application[];
  onUpdateApplicationStatus: (appId: number, newStatus: ApplicationStatus) => void;
  onAddApplicationNote: (appId: number, note: string) => void;
  onCreateJob: (newJob: Omit<Job, 'id' | 'createdAt'>) => void;
  onToggleJobActive: (jobId: number) => void;
}

export const AdminDashboardView: React.FC<AdminDashboardViewProps> = ({
  jobs,
  applications,
  onUpdateApplicationStatus,
  onAddApplicationNote,
  onCreateJob,
  onToggleJobActive
}) => {
  const [activeTab, setActiveTab] = useState<'pipeline' | 'jobs' | 'analytics'>('pipeline');
  const [statusFilter, setStatusFilter] = useState<string>('All');
  const [searchQuery, setSearchQuery] = useState('');
  const [newNoteInputs, setNewNoteInputs] = useState<Record<number, string>>({});

  // New Job Modal / Form State
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newTitle, setNewTitle] = useState('Senior Cloud Platform Engineer');
  const [newCompany, setNewCompany] = useState('Vanguard Cloud Systems (DEMO DATA)');
  const [newLocation, setNewLocation] = useState('Remote / US');
  const [newWorkMode, setNewWorkMode] = useState<'Remote' | 'Hybrid' | 'On-site'>('Remote');
  const [newLevel, setNewLevel] = useState('Senior (4+ years)');
  const [newSalary, setNewSalary] = useState('$135,000 - $165,000/yr');
  const [newSkills, setNewSkills] = useState('Go, Kubernetes, AWS, Terraform, Docker, CI/CD');
  const [newDesc, setNewDesc] = useState('Build reliable infrastructure services, manage multi-region Kubernetes clusters, and automate cloud provisioning pipelines. [DEMO DATA]');

  const handleCreateJobSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTitle || !newCompany || !newSkills) return;

    onCreateJob({
      title: newTitle,
      company: newCompany,
      location: newLocation,
      workMode: newWorkMode,
      experienceLevel: newLevel,
      salaryRange: newSalary,
      requiredSkills: newSkills,
      preferredQualifications: 'Prometheus, Grafana, Istio, Linux kernel tuning',
      description: newDesc,
      applicationUrl: 'https://example.com/careers/demo-job-new',
      isActive: true,
      isDemo: true
    });

    setShowCreateModal(false);
  };

  const handleAddNote = (appId: number) => {
    const text = newNoteInputs[appId]?.trim();
    if (!text) return;
    onAddApplicationNote(appId, text);
    setNewNoteInputs({ ...newNoteInputs, [appId]: '' });
  };

  const filteredApps = applications.filter(app => {
    if (statusFilter !== 'All' && app.status !== statusFilter) return false;
    if (searchQuery) {
      const q = searchQuery.toLowerCase();
      const matchName = app.candidateName.toLowerCase().includes(q);
      const matchJob = app.jobTitle.toLowerCase().includes(q);
      const matchEmail = app.candidateEmail.toLowerCase().includes(q);
      return matchName || matchJob || matchEmail;
    }
    return true;
  });

  const exportCSV = () => {
    const headers = ['App ID,Job Title,Company,Candidate Name,Candidate Email,Status,ATS Score,Date Applied'];
    const rows = filteredApps.map(a => 
      `"${a.id}","${a.jobTitle}","${a.company}","${a.candidateName}","${a.candidateEmail}","${a.status}","${a.atsMatchScore}%","${a.createdAt}"`
    );
    const csvContent = [headers, ...rows].join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'candidate_pipeline_export.csv';
    link.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-6">
      {/* Admin Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-purple-500/20 border border-purple-500/40 text-purple-300 text-[10px] font-bold uppercase tracking-wider mb-1">
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>Administrator & Recruiter Console</span>
          </div>
          <h1 className="text-xl md:text-2xl font-black text-white">Applicant Tracking System Operations</h1>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={exportCSV}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 text-xs font-semibold"
          >
            <Download className="w-3.5 h-3.5 text-cyan-400" />
            <span>Export CSV</span>
          </button>
          <button
            onClick={() => setShowCreateModal(true)}
            className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-gradient-to-r from-cyan-500 to-purple-600 hover:from-cyan-400 hover:to-purple-500 text-white text-xs font-bold shadow-md shadow-cyan-500/20"
          >
            <Plus className="w-3.5 h-3.5" />
            <span>Publish New Job</span>
          </button>
        </div>
      </div>

      {/* Admin KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="rounded-xl bg-[#0f1428]/80 border border-purple-900/30 p-4">
          <div className="text-[11px] font-semibold text-slate-400 uppercase">Total Candidates</div>
          <div className="text-2xl font-black text-white mt-1">2</div>
          <div className="text-[10px] text-cyan-400 mt-1">Active registered seekers</div>
        </div>
        <div className="rounded-xl bg-[#0f1428]/80 border border-purple-900/30 p-4">
          <div className="text-[11px] font-semibold text-slate-400 uppercase">Active Job Postings</div>
          <div className="text-2xl font-black text-white mt-1">{jobs.filter(j => j.isActive).length}</div>
          <div className="text-[10px] text-purple-300 mt-1">{jobs.length} total in system</div>
        </div>
        <div className="rounded-xl bg-[#0f1428]/80 border border-purple-900/30 p-4">
          <div className="text-[11px] font-semibold text-slate-400 uppercase">Total Applications</div>
          <div className="text-2xl font-black text-white mt-1">{applications.length}</div>
          <div className="text-[10px] text-emerald-400 mt-1">In ATS pipeline</div>
        </div>
        <div className="rounded-xl bg-[#0f1428]/80 border border-purple-900/30 p-4">
          <div className="text-[11px] font-semibold text-slate-400 uppercase">Average ATS Match</div>
          <div className="text-2xl font-black text-white mt-1">
            {applications.length > 0 
              ? `${Math.round(applications.reduce((acc, a) => acc + a.atsMatchScore, 0) / applications.length)}%` 
              : '82%'}
          </div>
          <div className="text-[10px] text-blue-400 mt-1">Algorithm compatibility</div>
        </div>
      </div>

      {/* Admin Tab Switcher */}
      <div className="flex gap-2 border-b border-purple-900/30 pb-2">
        <button
          onClick={() => setActiveTab('pipeline')}
          className={`px-4 py-1.5 rounded-lg text-xs font-bold transition-colors ${
            activeTab === 'pipeline'
              ? 'bg-purple-600/30 text-purple-200 border border-purple-500/40'
              : 'text-slate-400 hover:text-white'
          }`}
        >
          Candidate Pipeline & Status ({applications.length})
        </button>
        <button
          onClick={() => setActiveTab('jobs')}
          className={`px-4 py-1.5 rounded-lg text-xs font-bold transition-colors ${
            activeTab === 'jobs'
              ? 'bg-purple-600/30 text-purple-200 border border-purple-500/40'
              : 'text-slate-400 hover:text-white'
          }`}
        >
          Manage Jobs ({jobs.length})
        </button>
      </div>

      {/* Tab: Pipeline */}
      {activeTab === 'pipeline' && (
        <div className="space-y-4">
          {/* Search & Filters */}
          <div className="flex flex-col sm:flex-row gap-3">
            <div className="relative flex-1">
              <Search className="w-4 h-4 text-slate-500 absolute left-3 top-2.5" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search candidates, emails, or roles..."
                className="w-full pl-9 pr-3 py-2 rounded-xl bg-slate-900/80 border border-slate-700 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-cyan-400"
              />
            </div>

            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="rounded-xl bg-slate-900/80 border border-slate-700 px-3 py-2 text-xs text-white"
            >
              <option value="All">All Statuses</option>
              <option value="Applied">Applied</option>
              <option value="Under Review">Under Review</option>
              <option value="Shortlisted">Shortlisted</option>
              <option value="Interview">Interview</option>
              <option value="Selected">Selected</option>
              <option value="Rejected">Rejected</option>
            </select>
          </div>

          {/* Candidate Applications List */}
          <div className="space-y-3">
            {filteredApps.map(app => (
              <div 
                key={app.id}
                className="rounded-2xl bg-[#0f1428]/90 border border-purple-900/30 p-5 space-y-4"
              >
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                  <div>
                    <h3 className="text-base font-bold text-white">{app.candidateName}</h3>
                    <p className="text-xs text-cyan-400">
                      Applied for: <strong className="text-slate-200">{app.jobTitle}</strong> ({app.company})
                    </p>
                    <div className="text-[11px] text-slate-400 mt-1">
                      Email: {app.candidateEmail} • Date: {app.createdAt} • Resume: {app.resumeFilename}
                    </div>
                  </div>

                  <div className="flex items-center gap-4">
                    <div className="text-right">
                      <div className="text-[10px] text-slate-400 uppercase font-semibold">ATS Match</div>
                      <div className="text-lg font-black text-cyan-400">{app.atsMatchScore}%</div>
                    </div>

                    <div>
                      <label className="text-[10px] text-slate-400 block mb-1">Pipeline Stage:</label>
                      <select
                        value={app.status}
                        onChange={(e) => onUpdateApplicationStatus(app.id, e.target.value as ApplicationStatus)}
                        className="rounded-lg bg-slate-900 border border-cyan-500/40 text-cyan-300 text-xs font-semibold px-2.5 py-1"
                      >
                        <option value="Applied">Applied</option>
                        <option value="Under Review">Under Review</option>
                        <option value="Shortlisted">Shortlisted</option>
                        <option value="Interview">Interview</option>
                        <option value="Selected">Selected</option>
                        <option value="Rejected">Rejected</option>
                      </select>
                    </div>
                  </div>
                </div>

                {/* Confidential Recruiter Internal Notes */}
                <div className="rounded-xl bg-purple-950/20 border border-purple-500/20 p-3 space-y-2">
                  <div className="flex items-center gap-1.5 text-xs font-bold text-purple-300">
                    <Lock className="w-3.5 h-3.5 text-purple-400" />
                    <span>Confidential Recruiter Internal Notes (Strictly Hidden from Candidate)</span>
                  </div>

                  {app.notes && app.notes.length > 0 ? (
                    <div className="space-y-1.5">
                      {app.notes.map(note => (
                        <div key={note.id} className="p-2 rounded bg-slate-900/60 text-xs text-slate-200 border-l-2 border-purple-500">
                          <span className="font-semibold text-purple-300">{note.authorName} ({note.createdAt}): </span>
                          <span>{note.note}</span>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="text-[11px] text-slate-400 italic">No internal recruiter notes added yet.</div>
                  )}

                  <div className="flex gap-2 pt-1">
                    <input
                      type="text"
                      value={newNoteInputs[app.id] || ''}
                      onChange={(e) => setNewNoteInputs({ ...newNoteInputs, [app.id]: e.target.value })}
                      placeholder="Add private evaluation notes, interview questions, or next steps..."
                      className="flex-1 rounded-lg bg-slate-900/80 border border-slate-700 px-3 py-1.5 text-xs text-white focus:outline-none focus:border-purple-400"
                    />
                    <button
                      onClick={() => handleAddNote(app.id)}
                      className="px-3 py-1.5 rounded-lg bg-purple-600/40 hover:bg-purple-600/60 border border-purple-500/40 text-purple-200 text-xs font-semibold shrink-0"
                    >
                      Add Note
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab: Jobs Management */}
      {activeTab === 'jobs' && (
        <div className="space-y-4">
          <div className="space-y-3">
            {jobs.map(job => (
              <div 
                key={job.id}
                className="rounded-xl bg-[#0f1428]/90 border border-purple-900/30 p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3"
              >
                <div>
                  <div className="flex items-center gap-2">
                    <h4 className="text-sm font-bold text-white">{job.title}</h4>
                    {job.isDemo && (
                      <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-500/20 text-amber-300 border border-amber-500/40">
                        DEMO DATA
                      </span>
                    )}
                  </div>
                  <p className="text-xs text-cyan-400">
                    {job.company} • {job.location} ({job.workMode}) • {job.salaryRange}
                  </p>
                  <p className="text-[11px] text-slate-400 mt-1">
                    <strong>Skills:</strong> {job.requiredSkills}
                  </p>
                </div>

                <div className="flex items-center gap-3">
                  <span className={`text-xs font-semibold ${job.isActive ? 'text-emerald-400' : 'text-slate-500'}`}>
                    {job.isActive ? 'Active' : 'Inactive'}
                  </span>
                  <button
                    onClick={() => onToggleJobActive(job.id)}
                    className="p-1 text-slate-400 hover:text-white"
                  >
                    {job.isActive ? (
                      <ToggleRight className="w-6 h-6 text-emerald-400" />
                    ) : (
                      <ToggleLeft className="w-6 h-6 text-slate-600" />
                    )}
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Create Job Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="rounded-2xl bg-[#0e1329] border border-purple-500/40 w-full max-w-xl p-6 space-y-4 max-h-[90vh] overflow-y-auto">
            <h3 className="text-lg font-bold text-white">Create New Job Posting</h3>
            <form onSubmit={handleCreateJobSubmit} className="space-y-3">
              <div>
                <label className="text-xs text-slate-300 block mb-1">Job Title*</label>
                <input
                  type="text"
                  required
                  value={newTitle}
                  onChange={(e) => setNewTitle(e.target.value)}
                  className="w-full rounded-xl bg-slate-900 border border-slate-700 p-2 text-xs text-white"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-xs text-slate-300 block mb-1">Company*</label>
                  <input
                    type="text"
                    required
                    value={newCompany}
                    onChange={(e) => setNewCompany(e.target.value)}
                    className="w-full rounded-xl bg-slate-900 border border-slate-700 p-2 text-xs text-white"
                  />
                </div>
                <div>
                  <label className="text-xs text-slate-300 block mb-1">Location*</label>
                  <input
                    type="text"
                    required
                    value={newLocation}
                    onChange={(e) => setNewLocation(e.target.value)}
                    className="w-full rounded-xl bg-slate-900 border border-slate-700 p-2 text-xs text-white"
                  />
                </div>
              </div>

              <div className="grid grid-cols-3 gap-3">
                <div>
                  <label className="text-xs text-slate-300 block mb-1">Work Mode</label>
                  <select
                    value={newWorkMode}
                    onChange={(e) => setNewWorkMode(e.target.value as any)}
                    className="w-full rounded-xl bg-slate-900 border border-slate-700 p-2 text-xs text-white"
                  >
                    <option value="Remote">Remote</option>
                    <option value="Hybrid">Hybrid</option>
                    <option value="On-site">On-site</option>
                  </select>
                </div>
                <div>
                  <label className="text-xs text-slate-300 block mb-1">Experience Level</label>
                  <input
                    type="text"
                    value={newLevel}
                    onChange={(e) => setNewLevel(e.target.value)}
                    className="w-full rounded-xl bg-slate-900 border border-slate-700 p-2 text-xs text-white"
                  />
                </div>
                <div>
                  <label className="text-xs text-slate-300 block mb-1">Salary Range</label>
                  <input
                    type="text"
                    value={newSalary}
                    onChange={(e) => setNewSalary(e.target.value)}
                    className="w-full rounded-xl bg-slate-900 border border-slate-700 p-2 text-xs text-white"
                  />
                </div>
              </div>

              <div>
                <label className="text-xs text-slate-300 block mb-1">Required Skills (comma separated)*</label>
                <input
                  type="text"
                  required
                  value={newSkills}
                  onChange={(e) => setNewSkills(e.target.value)}
                  className="w-full rounded-xl bg-slate-900 border border-slate-700 p-2 text-xs text-white"
                />
              </div>

              <div>
                <label className="text-xs text-slate-300 block mb-1">Job Description*</label>
                <textarea
                  rows={3}
                  required
                  value={newDesc}
                  onChange={(e) => setNewDesc(e.target.value)}
                  className="w-full rounded-xl bg-slate-900 border border-slate-700 p-2 text-xs text-white font-mono"
                />
              </div>

              <div className="flex justify-end gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-400 hover:text-white"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 rounded-xl bg-gradient-to-r from-cyan-500 to-purple-600 hover:from-cyan-400 hover:to-purple-500 text-white text-xs font-bold"
                >
                  Publish Role
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
