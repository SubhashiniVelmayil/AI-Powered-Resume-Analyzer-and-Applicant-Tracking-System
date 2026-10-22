import React, { useState } from 'react';
import { 
  Upload, 
  FileText, 
  CheckCircle2, 
  AlertTriangle, 
  Sparkles, 
  Download, 
  ArrowRight, 
  RefreshCw,
  Info,
  ChevronDown,
  ChevronUp
} from 'lucide-react';
import { SAMPLE_RESUMES, analyzeResumeClient, rewriteBulletClient } from '../data/mockDatabase';
import { ResumeAnalysisResult } from '../types';

interface ResumeAnalyzerViewProps {
  onAnalyzedResume?: (text: string, filename: string) => void;
}

export const ResumeAnalyzerView: React.FC<ResumeAnalyzerViewProps> = ({ onAnalyzedResume }) => {
  const [selectedSampleIndex, setSelectedSampleIndex] = useState(0);
  const [resumeText, setResumeText] = useState(SAMPLE_RESUMES[0].text);
  const [filename, setFilename] = useState(SAMPLE_RESUMES[0].filename);
  const [analysis, setAnalysis] = useState<ResumeAnalysisResult | null>(() => analyzeResumeClient(SAMPLE_RESUMES[0].text));
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [scannedWarning, setScannedWarning] = useState<string | null>(null);

  // Bullet rewriter state
  const [inputBullet, setInputBullet] = useState('Worked on database performance and backend endpoints.');
  const [rewrittenBullet, setRewrittenBullet] = useState<{ original: string; improved: string; verb: string } | null>(null);

  // Handle sample selection
  const handleSelectSample = (index: number) => {
    setSelectedSampleIndex(index);
    const sample = SAMPLE_RESUMES[index];
    setFilename(sample.filename);
    setResumeText(sample.text);
    setScannedWarning(null);

    setIsAnalyzing(true);
    setTimeout(() => {
      const res = analyzeResumeClient(sample.text);
      setAnalysis(res);
      setIsAnalyzing(false);
      if (onAnalyzedResume) {
        onAnalyzedResume(sample.text, sample.filename);
      }
    }, 400);
  };

  // Handle file upload
  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (!file.name.toLowerCase().endsWith('.pdf') && !file.name.toLowerCase().endsWith('.txt')) {
      alert("Invalid file format. Please upload a PDF (.pdf) or text (.txt) file.");
      return;
    }

    if (file.size > 5 * 1024 * 1024) {
      alert("File size exceeds 5MB limit.");
      return;
    }

    setFilename(file.name);
    const reader = new FileReader();

    reader.onload = (event) => {
      const content = (event.target?.result as string) || '';
      // Simple text extract heuristic
      const cleanText = content.replace(/[^\x20-\x7E\t\r\n]/g, ' ').replace(/\s+/g, ' ').trim();

      if (cleanText.length < 60) {
        setScannedWarning(
          "⚠️ Scanned or Image-Only PDF Detected: Extracted text contains fewer than 60 characters. Optical Character Recognition (OCR) is required for scanned documents. You can paste your resume text manually below."
        );
        setResumeText("");
      } else {
        setScannedWarning(null);
        setResumeText(cleanText);
        runAnalysis(cleanText, file.name);
      }
    };

    reader.readAsText(file);
  };

  const runAnalysis = (textToAnalyze: string, fname: string) => {
    setIsAnalyzing(true);
    setTimeout(() => {
      const result = analyzeResumeClient(textToAnalyze);
      setAnalysis(result);
      setIsAnalyzing(false);
      if (onAnalyzedResume) {
        onAnalyzedResume(textToAnalyze, fname);
      }
    }, 500);
  };

  const handleRewrite = () => {
    if (!inputBullet.trim()) return;
    const res = rewriteBulletClient(inputBullet);
    setRewrittenBullet(res);
  };

  const downloadReport = () => {
    if (!analysis) return;
    const md = `# Resume Audit & ATS Diagnostic Report: ${analysis.candidateInfo.candidateName}
Generated via AI-Powered Resume Analyzer & ATS
Advisory Score: ${analysis.overallScore} / 100

## 1. Rubric Score Breakdown
- Content Quality: ${analysis.rubricBreakdown.contentQuality} / 25
- Skills Relevance: ${analysis.rubricBreakdown.skillsRelevance} / 20
- Projects & Experience: ${analysis.rubricBreakdown.projectsExperience} / 20
- Education & Certifications: ${analysis.rubricBreakdown.educationCertifications} / 10
- Measurable Impact: ${analysis.rubricBreakdown.achievementsImpact} / 15
- Readability & Structure: ${analysis.rubricBreakdown.readabilityStructure} / 10

## 2. Identified Competencies
Technical Skills: ${analysis.skills.technicalSkills.join(', ') || 'None detected'}
Soft Skills: ${analysis.skills.softSkills.join(', ') || 'None detected'}

## 3. Core Strengths
${analysis.strengths.map(s => `- **${s.title}**: ${s.detail}`).join('\n')}

## 4. Areas for Improvement
${analysis.weaknesses.map(w => `- **${w.title}**: ${w.detail}`).join('\n')}

## 5. ATS Formatting Audit
${analysis.atsChecks.map(c => `- [${c.passed ? 'PASS' : 'FLAG'}] ${c.check}: ${c.recommendation}`).join('\n')}
`;

    const blob = new Blob([md], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${analysis.candidateInfo.candidateName.replace(/\s+/g, '_')}_Resume_Report.md`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-6">
      {/* Header & Description */}
      <div>
        <h1 className="text-xl md:text-2xl font-black text-white">AI Resume Analyzer & Rubric Scoring</h1>
        <p className="text-xs text-slate-400 mt-1">
          Upload a resume or test with instant 1-click profiles to evaluate ATS formatting, extract technical skills, and calculate transparent scores.
        </p>
      </div>

      {/* 1-Click Sample Resumes & Upload Bar */}
      <div className="rounded-2xl bg-[#0f1428]/90 border border-purple-900/30 p-6 space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <label className="text-xs font-semibold text-slate-300 uppercase tracking-wider block mb-2">
              Select Pre-Loaded Sample Profile (Instant 1-Click Testing)
            </label>
            <div className="flex flex-wrap gap-2">
              {SAMPLE_RESUMES.map((sample, idx) => (
                <button
                  key={sample.filename}
                  onClick={() => handleSelectSample(idx)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                    selectedSampleIndex === idx
                      ? 'bg-gradient-to-r from-cyan-500 to-purple-600 text-white font-semibold shadow-md shadow-cyan-500/20'
                      : 'bg-slate-800/80 hover:bg-slate-700/80 text-slate-300 border border-slate-700'
                  }`}
                >
                  {sample.name.split(' - ')[0]}
                </button>
              ))}
            </div>
          </div>

          <div>
            <label className="text-xs font-semibold text-slate-300 uppercase tracking-wider block mb-2">
              Or Upload Your PDF Document
            </label>
            <label className="flex items-center gap-2 px-4 py-2 rounded-xl bg-purple-900/40 hover:bg-purple-800/50 border border-purple-500/40 text-purple-200 text-xs font-semibold cursor-pointer transition-colors">
              <Upload className="w-3.5 h-3.5 text-cyan-400" />
              <span>Choose PDF / Text File</span>
              <input
                type="file"
                accept=".pdf,.txt"
                onChange={handleFileUpload}
                className="hidden"
              />
            </label>
          </div>
        </div>

        {scannedWarning && (
          <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-200 text-xs">
            {scannedWarning}
          </div>
        )}

        {/* Text Area for manual edits */}
        <div className="space-y-2">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>Active Document: <strong className="text-cyan-400">{filename}</strong></span>
            <span>{resumeText.split(/\s+/).filter(Boolean).length} words</span>
          </div>
          <textarea
            value={resumeText}
            onChange={(e) => setResumeText(e.target.value)}
            rows={5}
            placeholder="Paste resume text directly here..."
            className="w-full rounded-xl bg-slate-900/80 border border-slate-800 focus:border-cyan-500/60 p-3 text-xs text-slate-200 focus:outline-none font-mono resize-y"
          />
          <button
            onClick={() => runAnalysis(resumeText, filename)}
            disabled={isAnalyzing}
            className="flex items-center gap-2 px-4 py-2 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white text-xs font-bold shadow-md shadow-cyan-500/20 disabled:opacity-50"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${isAnalyzing ? 'animate-spin' : ''}`} />
            <span>{isAnalyzing ? 'Evaluating Rubric...' : 'Re-Analyze Text'}</span>
          </button>
        </div>
      </div>

      {/* Analysis Results Display */}
      {analysis && (
        <div className="space-y-6">
          {/* Main Score Hero Card */}
          <div className="rounded-2xl bg-gradient-to-br from-[#121735]/90 via-[#18113c]/90 to-[#0e142b]/90 border border-purple-900/40 p-6 md:p-8 flex flex-col md:flex-row items-center justify-between gap-6">
            <div className="space-y-2 text-center md:text-left">
              <span className="text-xs font-bold text-cyan-400 uppercase tracking-widest">
                Comprehensive Diagnostic Benchmark
              </span>
              <h2 className="text-2xl font-black text-white">
                Candidate: {analysis.candidateInfo.candidateName}
              </h2>
              <p className="text-xs text-slate-300 max-w-xl">
                {analysis.disclaimer}
              </p>
              <div className="flex flex-wrap items-center gap-3 pt-2">
                <span className="text-xs text-slate-400">
                  Email: <strong className="text-slate-200">{analysis.candidateInfo.email || 'None'}</strong>
                </span>
                <span className="text-xs text-slate-400">•</span>
                <span className="text-xs text-slate-400">
                  Phone: <strong className="text-slate-200">{analysis.candidateInfo.phone || 'None'}</strong>
                </span>
                <span className="text-xs text-slate-400">•</span>
                <span className="text-xs text-slate-400">
                  Engine: <strong className="text-cyan-400">{analysis.provider}</strong>
                </span>
              </div>
            </div>

            {/* Circular Score Visual */}
            <div className="flex flex-col items-center shrink-0">
              <div className="w-28 h-28 rounded-full bg-slate-900/90 border-4 border-cyan-400 flex flex-col items-center justify-center shadow-2xl shadow-cyan-500/30">
                <span className="text-3xl font-black text-white leading-none">
                  {analysis.overallScore}
                </span>
                <span className="text-[10px] text-cyan-300 uppercase tracking-wider font-semibold mt-1">
                  out of 100
                </span>
              </div>
              <button
                onClick={downloadReport}
                className="mt-4 flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-purple-900/40 hover:bg-purple-800/60 border border-purple-500/40 text-purple-200 transition-colors"
              >
                <Download className="w-3.5 h-3.5 text-cyan-400" />
                <span>Download Report (.md)</span>
              </button>
            </div>
          </div>

          {/* 6-Part Transparent Rubric Breakdown */}
          <div className="rounded-2xl bg-[#0f1428]/80 border border-purple-900/30 p-6">
            <h3 className="text-base font-bold text-white mb-4">
              📊 Transparent Rubric Scoring Breakdown (100 Points Total)
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              <div className="rounded-xl bg-slate-900/60 border border-slate-800 p-4">
                <div className="flex justify-between items-center text-xs mb-1">
                  <span className="font-semibold text-slate-300">Content Quality</span>
                  <span className="font-bold text-cyan-400">{analysis.rubricBreakdown.contentQuality} / 25 pts</span>
                </div>
                <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                  <div className="bg-cyan-400 h-full rounded-full" style={{ width: `${(analysis.rubricBreakdown.contentQuality / 25) * 100}%` }} />
                </div>
                <p className="text-[11px] text-slate-400 mt-2">{analysis.explanations.contentQuality}</p>
              </div>

              <div className="rounded-xl bg-slate-900/60 border border-slate-800 p-4">
                <div className="flex justify-between items-center text-xs mb-1">
                  <span className="font-semibold text-slate-300">Skills Relevance</span>
                  <span className="font-bold text-purple-400">{analysis.rubricBreakdown.skillsRelevance} / 20 pts</span>
                </div>
                <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                  <div className="bg-purple-400 h-full rounded-full" style={{ width: `${(analysis.rubricBreakdown.skillsRelevance / 20) * 100}%` }} />
                </div>
                <p className="text-[11px] text-slate-400 mt-2">{analysis.explanations.skillsRelevance}</p>
              </div>

              <div className="rounded-xl bg-slate-900/60 border border-slate-800 p-4">
                <div className="flex justify-between items-center text-xs mb-1">
                  <span className="font-semibold text-slate-300">Projects & Experience</span>
                  <span className="font-bold text-blue-400">{analysis.rubricBreakdown.projectsExperience} / 20 pts</span>
                </div>
                <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                  <div className="bg-blue-400 h-full rounded-full" style={{ width: `${(analysis.rubricBreakdown.projectsExperience / 20) * 100}%` }} />
                </div>
                <p className="text-[11px] text-slate-400 mt-2">{analysis.explanations.projectsExperience}</p>
              </div>

              <div className="rounded-xl bg-slate-900/60 border border-slate-800 p-4">
                <div className="flex justify-between items-center text-xs mb-1">
                  <span className="font-semibold text-slate-300">Education & Certifications</span>
                  <span className="font-bold text-emerald-400">{analysis.rubricBreakdown.educationCertifications} / 10 pts</span>
                </div>
                <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                  <div className="bg-emerald-400 h-full rounded-full" style={{ width: `${(analysis.rubricBreakdown.educationCertifications / 10) * 100}%` }} />
                </div>
                <p className="text-[11px] text-slate-400 mt-2">{analysis.explanations.educationCertifications}</p>
              </div>

              <div className="rounded-xl bg-slate-900/60 border border-slate-800 p-4">
                <div className="flex justify-between items-center text-xs mb-1">
                  <span className="font-semibold text-slate-300">Measurable Impact</span>
                  <span className="font-bold text-amber-400">{analysis.rubricBreakdown.achievementsImpact} / 15 pts</span>
                </div>
                <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                  <div className="bg-amber-400 h-full rounded-full" style={{ width: `${(analysis.rubricBreakdown.achievementsImpact / 15) * 100}%` }} />
                </div>
                <p className="text-[11px] text-slate-400 mt-2">{analysis.explanations.achievementsImpact}</p>
              </div>

              <div className="rounded-xl bg-slate-900/60 border border-slate-800 p-4">
                <div className="flex justify-between items-center text-xs mb-1">
                  <span className="font-semibold text-slate-300">Readability & Structure</span>
                  <span className="font-bold text-cyan-400">{analysis.rubricBreakdown.readabilityStructure} / 10 pts</span>
                </div>
                <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                  <div className="bg-cyan-400 h-full rounded-full" style={{ width: `${(analysis.rubricBreakdown.readabilityStructure / 10) * 100}%` }} />
                </div>
                <p className="text-[11px] text-slate-400 mt-2">{analysis.explanations.readabilityStructure}</p>
              </div>
            </div>
          </div>

          {/* Strengths & Weaknesses Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            <div className="rounded-2xl bg-[#0f1428]/80 border border-emerald-900/30 p-6 space-y-3">
              <h3 className="text-sm font-bold text-emerald-400 flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4" />
                <span>Identified Core Strengths</span>
              </h3>
              {analysis.strengths.map((s, i) => (
                <div key={i} className="p-3 rounded-xl bg-emerald-950/20 border border-emerald-500/20">
                  <h4 className="text-xs font-bold text-emerald-300">{s.title}</h4>
                  <p className="text-xs text-slate-300 mt-0.5">{s.detail}</p>
                </div>
              ))}
            </div>

            <div className="rounded-2xl bg-[#0f1428]/80 border border-rose-900/30 p-6 space-y-3">
              <h3 className="text-sm font-bold text-rose-400 flex items-center gap-2">
                <AlertTriangle className="w-4 h-4" />
                <span>Areas for Improvement (Weaknesses)</span>
              </h3>
              {analysis.weaknesses.map((w, i) => (
                <div key={i} className="p-3 rounded-xl bg-rose-950/20 border border-rose-500/20">
                  <h4 className="text-xs font-bold text-rose-300">{w.title}</h4>
                  <p className="text-xs text-slate-300 mt-0.5">{w.detail}</p>
                </div>
              ))}
            </div>
          </div>

          {/* ATS Formatting Audit Checklist */}
          <div className="rounded-2xl bg-[#0f1428]/80 border border-purple-900/30 p-6">
            <h3 className="text-sm font-bold text-white mb-3">
              📋 ATS Parsing & Formatting Audit Checklist
            </h3>
            <div className="space-y-2">
              {analysis.atsChecks.map((chk, i) => (
                <div key={i} className="flex items-start gap-3 p-3 rounded-xl bg-slate-900/50 border border-slate-800">
                  <div className="mt-0.5">
                    {chk.passed ? (
                      <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                    ) : (
                      <AlertTriangle className="w-4 h-4 text-amber-400" />
                    )}
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-bold text-white">{chk.check}</span>
                      <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full ${
                        chk.passed ? 'bg-emerald-500/20 text-emerald-300' : 'bg-amber-500/20 text-amber-300'
                      }`}>
                        {chk.passed ? 'PASS' : chk.severity.toUpperCase()}
                      </span>
                    </div>
                    {chk.issue && <p className="text-xs text-rose-400 mt-0.5 font-medium">{chk.issue}</p>}
                    <p className="text-xs text-slate-400 mt-0.5">{chk.recommendation}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* AI Bullet Point Rewriter Tool */}
          <div className="rounded-2xl bg-gradient-to-r from-purple-950/40 via-[#141838] to-purple-950/40 border border-purple-500/30 p-6 space-y-4">
            <div className="flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-cyan-400" />
              <h3 className="text-sm font-bold text-white">
                AI Bullet Point Rewriter (Google XYZ Formula)
              </h3>
            </div>
            <p className="text-xs text-slate-300">
              Converts passive phrases into measurable accomplishment statements: <em>"Accomplished [X] as measured by [Y] by doing [Z]"</em> with strict placeholder guardrails.
            </p>

            <div className="flex flex-col sm:flex-row gap-3">
              <input
                type="text"
                value={inputBullet}
                onChange={(e) => setInputBullet(e.target.value)}
                placeholder="Enter a resume bullet point..."
                className="flex-1 rounded-xl bg-slate-900/80 border border-slate-700 px-4 py-2 text-xs text-white focus:outline-none focus:border-cyan-400"
              />
              <button
                onClick={handleRewrite}
                className="px-4 py-2 rounded-xl bg-gradient-to-r from-cyan-500 to-purple-600 hover:from-cyan-400 hover:to-purple-500 text-white text-xs font-bold shrink-0 transition-all shadow-md shadow-cyan-500/20"
              >
                Rewrite Bullet Point
              </button>
            </div>

            {rewrittenBullet && (
              <div className="rounded-xl bg-slate-900/90 border border-purple-500/30 p-4 space-y-3">
                <div>
                  <div className="text-[10px] font-bold text-rose-400 uppercase tracking-wider">Original (Passive)</div>
                  <div className="text-xs text-slate-400 line-through mt-0.5">{rewrittenBullet.original}</div>
                </div>
                <div>
                  <div className="text-[10px] font-bold text-emerald-400 uppercase tracking-wider">Enhanced (Google XYZ Structure)</div>
                  <div className="text-xs text-emerald-300 font-medium mt-0.5">{rewrittenBullet.improved}</div>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
