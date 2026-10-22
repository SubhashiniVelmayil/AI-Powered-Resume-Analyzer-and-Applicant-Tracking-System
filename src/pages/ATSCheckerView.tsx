import React, { useState } from 'react';
import { Target, CheckCircle2, AlertTriangle, ArrowRight, Download, RefreshCw, Sparkles } from 'lucide-react';
import { Job, ATSScoreResult } from '../types';
import { compareResumeToJobClient, SAMPLE_RESUMES } from '../data/mockDatabase';

interface ATSCheckerViewProps {
  jobs: Job[];
  currentResumeText: string;
}

export const ATSCheckerView: React.FC<ATSCheckerViewProps> = ({ jobs, currentResumeText }) => {
  const [selectedJobId, setSelectedJobId] = useState<number>(jobs[0]?.id || 1);
  const [customJobMode, setCustomJobMode] = useState(false);
  const [customTitle, setCustomTitle] = useState('Senior Full Stack Engineer');
  const [customCompany, setCustomCompany] = useState('TechCorp Global');
  const [customRequiredSkills, setCustomRequiredSkills] = useState('Python, React, TypeScript, SQL, Docker, AWS');
  const [customDescription, setCustomDescription] = useState('Seeking an experienced full-stack engineer to architect modern microservices and high-throughput cloud web applications.');

  const [resumeText, setResumeText] = useState(currentResumeText || SAMPLE_RESUMES[0].text);
  const activeJob = jobs.find(j => j.id === selectedJobId) || jobs[0];

  const [result, setResult] = useState<ATSScoreResult | null>(() => {
    return compareResumeToJobClient(
      resumeText,
      activeJob.title,
      activeJob.description,
      activeJob.requiredSkills
    );
  });

  const handleRunComparison = () => {
    const title = customJobMode ? customTitle : activeJob.title;
    const desc = customJobMode ? customDescription : activeJob.description;
    const req = customJobMode ? customRequiredSkills : activeJob.requiredSkills;

    const res = compareResumeToJobClient(resumeText, title, desc, req);
    setResult(res);
  };

  const downloadReport = () => {
    if (!result) return;
    const title = customJobMode ? customTitle : activeJob.title;
    const company = customJobMode ? customCompany : activeJob.company;

    const md = `# ATS Role Compatibility Report: ${title} at ${company}
Estimated Compatibility Score: ${result.overallMatchScore} / 100

## 1. ATS Scoring Rubric Breakdown
- Required Skill Coverage: ${result.scoreBreakdown.requiredSkills} / 40 pts
- Experience & Project Evidence: ${result.scoreBreakdown.experienceEvidence} / 25 pts
- Education & Qualifications: ${result.scoreBreakdown.educationMatch} / 15 pts
- Job Description Keywords: ${result.scoreBreakdown.keywordCoverage} / 15 pts
- Certifications Alignment: ${result.scoreBreakdown.certificationsMatch} / 5 pts

## 2. Matched Skills (${result.matchedSkills.length})
${result.matchedSkills.join(', ') || 'None directly matched'}

## 3. Related Skills (${result.relatedSkills.length})
${result.relatedSkills.join(', ') || 'None'}

## 4. Missing Skills (${result.missingSkills.length})
${result.missingSkills.join(', ') || 'None'}

## 5. Strategic Recommendations
${result.recommendations.map(r => `- ${r}`).join('\n')}
`;

    const blob = new Blob([md], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${title.replace(/\s+/g, '_')}_ATS_Report.md`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl md:text-2xl font-black text-white">Job-Specific ATS Compatibility Checker</h1>
        <p className="text-xs text-slate-400 mt-1">
          Measure semantic alignment, uncover missing keywords, and review a 100-point rubric tailored to specific job vacancies.
        </p>
      </div>

      {/* Target Job Selector & Resume Inputs */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        {/* Job Selection Column */}
        <div className="rounded-2xl bg-[#0f1428]/90 border border-purple-900/30 p-6 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              <Target className="w-4 h-4 text-purple-400" />
              <span>Target Job Requirements</span>
            </h3>
            <button
              onClick={() => {
                setCustomJobMode(!customJobMode);
                setTimeout(handleRunComparison, 50);
              }}
              className="text-xs font-semibold text-cyan-400 hover:text-cyan-300"
            >
              {customJobMode ? 'Select from Curated Jobs' : 'Paste Custom Job'}
            </button>
          </div>

          {!customJobMode ? (
            <div className="space-y-3">
              <label className="text-xs text-slate-400 block">Choose Active Job Listing:</label>
              <select
                value={selectedJobId}
                onChange={(e) => {
                  setSelectedJobId(Number(e.target.value));
                  setTimeout(handleRunComparison, 50);
                }}
                className="w-full rounded-xl bg-slate-900/90 border border-slate-700 p-2.5 text-xs text-white focus:outline-none focus:border-cyan-400"
              >
                {jobs.map(j => (
                  <option key={j.id} value={j.id}>
                    {j.title} — {j.company} ({j.workMode})
                  </option>
                ))}
              </select>

              <div className="p-3 rounded-xl bg-slate-900/50 border border-slate-800 text-xs space-y-1.5">
                <div><strong className="text-slate-300">Required Skills:</strong> <span className="text-cyan-300">{activeJob.requiredSkills}</span></div>
                <div><strong className="text-slate-300">Location:</strong> {activeJob.location} ({activeJob.workMode})</div>
                <div><strong className="text-slate-300">Compensation:</strong> {activeJob.salaryRange}</div>
              </div>
            </div>
          ) : (
            <div className="space-y-3">
              <input
                type="text"
                value={customTitle}
                onChange={(e) => setCustomTitle(e.target.value)}
                placeholder="Job Title"
                className="w-full rounded-xl bg-slate-900/90 border border-slate-700 p-2 text-xs text-white"
              />
              <input
                type="text"
                value={customRequiredSkills}
                onChange={(e) => setCustomRequiredSkills(e.target.value)}
                placeholder="Required Skills (comma separated)"
                className="w-full rounded-xl bg-slate-900/90 border border-slate-700 p-2 text-xs text-white"
              />
              <textarea
                value={customDescription}
                onChange={(e) => setCustomDescription(e.target.value)}
                placeholder="Full Job Description"
                rows={3}
                className="w-full rounded-xl bg-slate-900/90 border border-slate-700 p-2 text-xs text-white font-mono"
              />
            </div>
          )}
        </div>

        {/* Resume Input Column */}
        <div className="rounded-2xl bg-[#0f1428]/90 border border-purple-900/30 p-6 space-y-3">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-bold text-white">Resume Text Evaluated</h3>
            <span className="text-xs text-slate-400">{resumeText.split(/\s+/).filter(Boolean).length} words</span>
          </div>
          <textarea
            value={resumeText}
            onChange={(e) => setResumeText(e.target.value)}
            rows={5}
            placeholder="Paste resume text to compare..."
            className="w-full rounded-xl bg-slate-900/90 border border-slate-700 p-2.5 text-xs text-slate-200 focus:outline-none focus:border-cyan-400 font-mono"
          />
          <button
            onClick={handleRunComparison}
            className="w-full py-2.5 rounded-xl bg-gradient-to-r from-purple-600 via-indigo-600 to-cyan-500 hover:from-purple-500 hover:to-cyan-400 text-white text-xs font-bold shadow-lg shadow-purple-500/20 transition-all"
          >
            Run ATS Compatibility Assessment
          </button>
        </div>
      </div>

      {/* Comparison Results */}
      {result && (
        <div className="space-y-6">
          {/* Hero Score Banner */}
          <div className="rounded-2xl bg-gradient-to-br from-[#121735]/90 via-[#18113c]/90 to-[#0e142b]/90 border border-purple-900/40 p-6 flex flex-col sm:flex-row items-center justify-between gap-6">
            <div className="space-y-1.5 text-center sm:text-left">
              <span className="text-xs font-bold text-purple-400 uppercase tracking-widest">
                Job Alignment Benchmark
              </span>
              <h2 className="text-xl md:text-2xl font-black text-white">
                {customJobMode ? customTitle : activeJob.title}
              </h2>
              <p className="text-xs text-slate-300 max-w-xl">
                {result.disclaimer}
              </p>
            </div>

            <div className="flex flex-col items-center shrink-0">
              <div className="w-24 h-24 rounded-full bg-slate-900/90 border-4 border-purple-500 flex flex-col items-center justify-center shadow-xl shadow-purple-500/30">
                <span className="text-2xl font-black text-white leading-none">
                  {result.overallMatchScore}%
                </span>
                <span className="text-[9px] text-purple-300 uppercase tracking-wider font-semibold mt-1">
                  Match
                </span>
              </div>
              <button
                onClick={downloadReport}
                className="mt-3 flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-semibold bg-purple-900/40 hover:bg-purple-800/60 border border-purple-500/40 text-purple-200"
              >
                <Download className="w-3.5 h-3.5 text-cyan-400" />
                <span>Export Report</span>
              </button>
            </div>
          </div>

          {/* Rubric Breakdown (40 / 25 / 15 / 15 / 5) */}
          <div className="rounded-2xl bg-[#0f1428]/80 border border-purple-900/30 p-6">
            <h3 className="text-sm font-bold text-white mb-4">
              🎯 100-Point ATS Compatibility Rubric Breakdown
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-5 gap-3">
              <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 text-center">
                <div className="text-[11px] text-slate-400">Required Skills</div>
                <div className="text-lg font-black text-cyan-400 mt-1">{result.scoreBreakdown.requiredSkills} / 40</div>
              </div>
              <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 text-center">
                <div className="text-[11px] text-slate-400">Experience Evidence</div>
                <div className="text-lg font-black text-purple-400 mt-1">{result.scoreBreakdown.experienceEvidence} / 25</div>
              </div>
              <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 text-center">
                <div className="text-[11px] text-slate-400">Education Match</div>
                <div className="text-lg font-black text-emerald-400 mt-1">{result.scoreBreakdown.educationMatch} / 15</div>
              </div>
              <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 text-center">
                <div className="text-[11px] text-slate-400">Keyword Coverage</div>
                <div className="text-lg font-black text-blue-400 mt-1">{result.scoreBreakdown.keywordCoverage} / 15</div>
              </div>
              <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 text-center">
                <div className="text-[11px] text-slate-400">Certifications</div>
                <div className="text-lg font-black text-amber-400 mt-1">{result.scoreBreakdown.certificationsMatch} / 5</div>
              </div>
            </div>
          </div>

          {/* Matched, Related, and Missing Skills */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
            <div className="rounded-2xl bg-[#0f1428]/80 border border-emerald-900/30 p-5 space-y-2">
              <h4 className="text-xs font-bold text-emerald-400 uppercase tracking-wider flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4" />
                <span>Exact Matched Skills ({result.matchedSkills.length})</span>
              </h4>
              <div className="flex flex-wrap gap-1.5 pt-2">
                {result.matchedSkills.length > 0 ? (
                  result.matchedSkills.map(m => (
                    <span key={m} className="px-2.5 py-1 rounded-lg bg-emerald-950/40 border border-emerald-500/30 text-emerald-300 text-xs font-medium">
                      {m}
                    </span>
                  ))
                ) : (
                  <span className="text-xs text-slate-500">No exact matches found.</span>
                )}
              </div>
            </div>

            <div className="rounded-2xl bg-[#0f1428]/80 border border-cyan-900/30 p-5 space-y-2">
              <h4 className="text-xs font-bold text-cyan-400 uppercase tracking-wider flex items-center gap-1.5">
                <Sparkles className="w-4 h-4" />
                <span>Related Competencies ({result.relatedSkills.length})</span>
              </h4>
              <div className="flex flex-wrap gap-1.5 pt-2">
                {result.relatedSkills.length > 0 ? (
                  result.relatedSkills.map(r => (
                    <span key={r} className="px-2.5 py-1 rounded-lg bg-cyan-950/40 border border-cyan-500/30 text-cyan-300 text-xs font-medium">
                      {r}
                    </span>
                  ))
                ) : (
                  <span className="text-xs text-slate-500">No related competencies detected.</span>
                )}
              </div>
            </div>

            <div className="rounded-2xl bg-[#0f1428]/80 border border-rose-900/30 p-5 space-y-2">
              <h4 className="text-xs font-bold text-rose-400 uppercase tracking-wider flex items-center gap-1.5">
                <AlertTriangle className="w-4 h-4" />
                <span>Missing Key Skills ({result.missingSkills.length})</span>
              </h4>
              <div className="flex flex-wrap gap-1.5 pt-2">
                {result.missingSkills.length > 0 ? (
                  result.missingSkills.map(gap => (
                    <span key={gap} className="px-2.5 py-1 rounded-lg bg-rose-950/40 border border-rose-500/30 text-rose-300 text-xs font-medium">
                      {gap}
                    </span>
                  ))
                ) : (
                  <span className="text-xs text-emerald-400">All required skills present!</span>
                )}
              </div>
            </div>
          </div>

          {/* Strategic Recommendations */}
          <div className="rounded-2xl bg-[#0f1428]/80 border border-purple-900/30 p-6 space-y-3">
            <h3 className="text-sm font-bold text-white">
              💡 Actionable Recommendations to Maximize Match
            </h3>
            <div className="space-y-2">
              {result.recommendations.map((rec, i) => (
                <div key={i} className="p-3 rounded-xl bg-purple-950/20 border border-purple-500/20 text-xs text-slate-200">
                  {rec}
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
