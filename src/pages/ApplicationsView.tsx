import React, { useState } from 'react';
import { Send, Clock, Calendar, CheckCircle2, ChevronRight, Filter } from 'lucide-react';
import { Application, ApplicationStatus } from '../types';

interface ApplicationsViewProps {
  applications: Application[];
  onNavigateToJobs: () => void;
}

export const ApplicationsView: React.FC<ApplicationsViewProps> = ({
  applications,
  onNavigateToJobs
}) => {
  const [selectedFilter, setSelectedFilter] = useState<string>('All');

  const filtered = applications.filter(app => {
    if (selectedFilter === 'All') return true;
    return app.status === selectedFilter;
  });

  const getStatusBadge = (status: ApplicationStatus) => {
    switch (status) {
      case 'Selected':
        return 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40';
      case 'Interview':
        return 'bg-cyan-500/20 text-cyan-300 border-cyan-500/40';
      case 'Shortlisted':
        return 'bg-purple-500/20 text-purple-300 border-purple-500/40';
      case 'Under Review':
        return 'bg-amber-500/20 text-amber-300 border-amber-500/40';
      case 'Rejected':
        return 'bg-rose-500/20 text-rose-300 border-rose-500/40';
      default:
        return 'bg-blue-500/20 text-blue-300 border-blue-500/40';
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl md:text-2xl font-black text-white">My Application Pipeline</h1>
          <p className="text-xs text-slate-400 mt-1">
            Track stages, timestamps, and estimated ATS match scores for every submitted role.
          </p>
        </div>

        <button
          onClick={onNavigateToJobs}
          className="px-4 py-2 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white text-xs font-bold shrink-0 shadow-md shadow-cyan-500/20 transition-all"
        >
          Browse Open Positions
        </button>
      </div>

      {/* Filter Tabs */}
      <div className="flex flex-wrap gap-2 p-1.5 rounded-xl bg-[#0f1428]/80 border border-purple-900/30">
        {['All', 'Applied', 'Under Review', 'Shortlisted', 'Interview', 'Selected', 'Rejected'].map(status => (
          <button
            key={status}
            onClick={() => setSelectedFilter(status)}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
              selectedFilter === status
                ? 'bg-purple-600/40 text-purple-200 border border-purple-500/40'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'
            }`}
          >
            {status}
          </button>
        ))}
      </div>

      {/* Application Cards */}
      {filtered.length === 0 ? (
        <div className="rounded-2xl bg-[#0f1428]/80 border border-purple-900/30 p-12 text-center space-y-3">
          <Send className="w-10 h-10 text-slate-600 mx-auto" />
          <h3 className="text-sm font-bold text-white">No Applications Found</h3>
          <p className="text-xs text-slate-400 max-w-sm mx-auto">
            You don't have any applications under the "{selectedFilter}" status filter.
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {filtered.map(app => (
            <div
              key={app.id}
              className="rounded-2xl bg-gradient-to-r from-[#11162e]/90 to-[#0e1329]/90 border border-purple-900/30 p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4"
            >
              <div className="space-y-1">
                <div className="flex items-center gap-2.5">
                  <h3 className="text-sm font-bold text-white">{app.jobTitle}</h3>
                  <span className={`text-[10px] font-bold px-2.5 py-0.5 rounded-full uppercase tracking-wider border ${getStatusBadge(app.status)}`}>
                    {app.status}
                  </span>
                </div>
                <div className="text-xs text-cyan-400 font-medium">
                  {app.company}
                </div>
                <div className="flex items-center gap-4 text-[11px] text-slate-400 pt-1">
                  <span className="flex items-center gap-1">
                    <Calendar className="w-3 h-3 text-slate-500" />
                    <span>Applied on {app.createdAt}</span>
                  </span>
                  <span>•</span>
                  <span>Resume: {app.resumeFilename}</span>
                </div>
              </div>

              <div className="flex items-center gap-5 shrink-0 self-end sm:self-auto">
                <div className="text-right">
                  <div className="text-[10px] text-slate-400 uppercase font-semibold">ATS Compatibility</div>
                  <div className="text-xl font-black text-cyan-400">{app.atsMatchScore}%</div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
