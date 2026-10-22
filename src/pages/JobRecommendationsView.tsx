import React, { useState } from 'react';
import { Briefcase, CheckCircle2, AlertTriangle, ArrowRight, Sparkles, Filter, ExternalLink } from 'lucide-react';
import { Job, Application } from '../types';
import { compareResumeToJobClient } from '../data/mockDatabase';

interface JobRecommendationsViewProps {
  jobs: Job[];
  currentResumeText: string;
  applications: Application[];
  onApply: (job: Job, matchScore: number) => void;
}

export const JobRecommendationsView: React.FC<JobRecommendationsViewProps> = ({
  jobs,
  currentResumeText,
  applications,
  onApply
}) => {
  const [workModeFilter, setWorkModeFilter] = useState<string>('All');
  const [minScore, setMinScore] = useState<number>(40);

  const appliedJobIds = new Set(applications.map(a => a.jobId));

  // Compute recommendations
  const rankedJobs = jobs
    .filter(j => j.isActive)
    .map(job => {
      const comp = compareResumeToJobClient(
        currentResumeText,
        job.title,
        job.description,
        job.requiredSkills
      );
      return {
        job,
        matchScore: comp.overallMatchScore,
        matchedSkills: comp.matchedSkills,
        missingSkills: comp.missingSkills,
        relatedSkills: comp.relatedSkills
      };
    })
    .sort((a, b) => b.matchScore - a.matchScore);

  const filteredJobs = rankedJobs.filter(item => {
    if (workModeFilter !== 'All' && item.job.workMode !== workModeFilter) {
      return false;
    }
    return item.matchScore >= minScore;
  });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl md:text-2xl font-black text-white">Smart Career & Job Recommendations</h1>
        <p className="text-xs text-slate-400 mt-1">
          Opportunities dynamically ranked by compatibility with your current resume competencies, complete with tailored learning pathways.
        </p>
      </div>

      {/* Filter Toolbar */}
      <div className="rounded-2xl bg-[#0f1428]/80 border border-purple-900/30 p-4 flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-3 w-full md:w-auto">
          <Filter className="w-4 h-4 text-cyan-400 shrink-0" />
          <span className="text-xs font-semibold text-slate-300">Filter Work Mode:</span>
          <div className="flex gap-1.5">
            {['All', 'Remote', 'Hybrid', 'On-site'].map(mode => (
              <button
                key={mode}
                onClick={() => setWorkModeFilter(mode)}
                className={`px-3 py-1 rounded-lg text-xs font-medium transition-colors ${
                  workModeFilter === mode
                    ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40'
                    : 'bg-slate-800/60 text-slate-400 hover:text-slate-200'
                }`}
              >
                {mode}
              </button>
            ))}
          </div>
        </div>

        <div className="flex items-center gap-3 w-full md:w-auto justify-end">
          <span className="text-xs text-slate-400">Min Match: <strong className="text-cyan-400">{minScore}%</strong></span>
          <input
            type="range"
            min={0}
            max={100}
            step={5}
            value={minScore}
            onChange={(e) => setMinScore(Number(e.target.value))}
            className="w-32 accent-cyan-400"
          />
        </div>
      </div>

      {/* Recommended Jobs List */}
      <div className="space-y-4">
        {filteredJobs.length === 0 ? (
          <div className="rounded-2xl bg-[#0f1428]/80 border border-purple-900/30 p-8 text-center text-xs text-slate-400">
            No job recommendations found matching the selected threshold ({minScore}%) and work mode ({workModeFilter}). Try lowering the minimum match percentage.
          </div>
        ) : (
          filteredJobs.map(({ job, matchScore, matchedSkills, missingSkills, relatedSkills }) => {
            const isApplied = appliedJobIds.has(job.id);

            return (
              <div 
                key={job.id}
                className="rounded-2xl bg-gradient-to-b from-[#11162e]/90 to-[#0c1024]/90 border border-purple-900/30 hover:border-cyan-500/40 p-6 transition-all duration-300 hover:shadow-xl hover:shadow-cyan-500/5 space-y-4"
              >
                {/* Header */}
                <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-3">
                  <div>
                    <div className="flex items-center gap-2">
                      <h3 className="text-base font-bold text-white">{job.title}</h3>
                      {job.isDemo && (
                        <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-500/20 text-amber-300 border border-amber-500/40">
                          DEMO DATA
                        </span>
                      )}
                    </div>
                    <div className="text-xs text-cyan-400 font-semibold mt-0.5">
                      {job.company} • <span className="text-slate-400 font-normal">{job.location} ({job.workMode})</span>
                    </div>
                  </div>

                  <div className="text-right shrink-0">
                    <div className="text-2xl font-black text-cyan-400">{matchScore}%</div>
                    <div className="text-[10px] text-slate-400 uppercase tracking-wider font-semibold">Match Score</div>
                  </div>
                </div>

                <div className="text-xs text-slate-300 flex flex-wrap gap-x-4 gap-y-1">
                  <span><strong>Salary:</strong> {job.salaryRange}</span>
                  <span>•</span>
                  <span><strong>Experience:</strong> {job.experienceLevel}</span>
                  <span>•</span>
                  <span><strong>Required:</strong> {job.requiredSkills}</span>
                </div>

                <p className="text-xs text-slate-400 leading-relaxed">
                  {job.description}
                </p>

                {/* Match Rationale & Suggested Learning Path */}
                <div className="rounded-xl bg-slate-900/70 border border-slate-800 p-3 space-y-2 text-xs">
                  <div>
                    <span className="font-bold text-cyan-400">Why Recommended: </span>
                    <span className="text-slate-200">
                      Strong foundation in {matchedSkills.slice(0, 3).join(', ') || 'core software fundamentals'}.
                    </span>
                  </div>

                  {missingSkills.length > 0 && (
                    <div>
                      <span className="font-bold text-purple-400">Suggested Learning Path: </span>
                      <span className="text-slate-300">
                        {missingSkills.slice(0, 2).map(m => `Build a portfolio project with ${m}`).join(' • ')}
                      </span>
                    </div>
                  )}

                  <div className="pt-1 flex flex-wrap gap-2 text-[11px]">
                    <span className="text-emerald-400 font-semibold">
                      Matched: {matchedSkills.join(', ') || 'None'}
                    </span>
                    {missingSkills.length > 0 && (
                      <span className="text-rose-400 font-semibold">
                        Gaps: {missingSkills.join(', ')}
                      </span>
                    )}
                  </div>
                </div>

                {/* Actions */}
                <div className="flex flex-wrap items-center justify-between gap-3 pt-1 border-t border-slate-800/80">
                  <div className="text-[11px] text-slate-500">
                    Application tracked inside ATS system upon submission
                  </div>

                  <div className="flex items-center gap-3">
                    <a
                      href={job.applicationUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-center gap-1 text-xs text-slate-400 hover:text-slate-200"
                    >
                      <span>Posting Details</span>
                      <ExternalLink className="w-3 h-3" />
                    </a>

                    <button
                      onClick={() => onApply(job, matchScore)}
                      disabled={isApplied}
                      className={`flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-bold transition-all ${
                        isApplied
                          ? 'bg-slate-800 text-slate-400 cursor-not-allowed border border-slate-700'
                          : 'bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white shadow-md shadow-cyan-500/20'
                      }`}
                    >
                      <CheckCircle2 className="w-3.5 h-3.5" />
                      <span>{isApplied ? 'Applied' : 'Submit Application (ATS)'}</span>
                    </button>
                  </div>
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};
