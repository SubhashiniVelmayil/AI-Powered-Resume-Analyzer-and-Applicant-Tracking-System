import React from 'react';
import { UserRole } from '../types';
import { UserCircle, Shield, Key, Terminal, Lock, CheckCircle2 } from 'lucide-react';

interface ProfileViewProps {
  userRole: UserRole;
  userName: string;
  onToggleRole: () => void;
  onOpenPythonModal: () => void;
}

export const ProfileView: React.FC<ProfileViewProps> = ({
  userRole,
  userName,
  onToggleRole,
  onOpenPythonModal
}) => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl md:text-2xl font-black text-white">Profile & System Settings</h1>
        <p className="text-xs text-slate-400 mt-1">
          Manage credentials, security preferences, AI API configurations, and view backend verification status.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        {/* Account Profile Card */}
        <div className="rounded-2xl bg-[#0f1428]/90 border border-purple-900/30 p-6 space-y-4">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-xl bg-purple-500/20 border border-purple-500/40 flex items-center justify-center text-purple-300">
              <UserCircle className="w-7 h-7" />
            </div>
            <div>
              <h3 className="text-base font-bold text-white">{userName}</h3>
              <p className="text-xs text-slate-400">alex.morgan@example.com</p>
            </div>
          </div>

          <div className="space-y-2 pt-2 border-t border-slate-800 text-xs">
            <div className="flex justify-between py-1">
              <span className="text-slate-400">Current Role:</span>
              <span className={`font-bold px-2.5 py-0.5 rounded-full ${
                userRole === 'admin' ? 'bg-purple-500/20 text-purple-300' : 'bg-cyan-500/20 text-cyan-300'
              }`}>
                {userRole === 'admin' ? '👑 Administrator / Recruiter' : '👤 Job Seeker / Candidate'}
              </span>
            </div>
            <div className="flex justify-between py-1">
              <span className="text-slate-400">Account ID:</span>
              <span className="font-mono text-slate-300">#USR-2026-88</span>
            </div>
            <div className="flex justify-between py-1">
              <span className="text-slate-400">Password Hashing:</span>
              <span className="text-emerald-400 font-semibold flex items-center gap-1">
                <CheckCircle2 className="w-3.5 h-3.5" />
                <span>PBKDF2-HMAC-SHA256 (100k rounds)</span>
              </span>
            </div>
          </div>

          <button
            onClick={onToggleRole}
            className="w-full py-2.5 rounded-xl bg-purple-900/40 hover:bg-purple-800/50 border border-purple-500/40 text-purple-200 text-xs font-semibold flex items-center justify-center gap-2 transition-colors"
          >
            <Shield className="w-4 h-4 text-purple-400" />
            <span>Switch Role to {userRole === 'admin' ? 'Job Seeker' : 'Administrator'}</span>
          </button>
        </div>

        {/* AI & API Configurations */}
        <div className="rounded-2xl bg-[#0f1428]/90 border border-purple-900/30 p-6 space-y-4">
          <div className="flex items-center gap-2">
            <Key className="w-5 h-5 text-cyan-400" />
            <h3 className="text-base font-bold text-white">AI Engine & Cloud API Integration</h3>
          </div>

          <div className="space-y-2 text-xs">
            <div className="flex justify-between py-1">
              <span className="text-slate-400">Active Engine:</span>
              <span className="text-cyan-400 font-semibold">Local Rule-Based & Rubric Engine</span>
            </div>
            <div className="flex justify-between py-1">
              <span className="text-slate-400">Groq API Status:</span>
              <span className="text-slate-400 font-mono">Optional (llama-3.3-70b-versatile)</span>
            </div>
            <div className="flex justify-between py-1">
              <span className="text-slate-400">Fallback Protection:</span>
              <span className="text-emerald-400 font-semibold">100% Operational Offline</span>
            </div>
          </div>

          <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800 text-[11px] text-slate-300 space-y-1">
            <strong className="text-cyan-400">How to configure Groq Cloud API:</strong>
            <p>1. Sign up for a free key at <code>console.groq.com</code></p>
            <p>2. Set <code>GROQ_API_KEY="your_key"</code> in <code>.env</code></p>
            <p>3. Application will seamlessly leverage cloud LLM inference</p>
          </div>

          <button
            onClick={onOpenPythonModal}
            className="w-full py-2.5 rounded-xl bg-slate-800/80 hover:bg-slate-700/80 border border-slate-700 text-slate-200 text-xs font-semibold flex items-center justify-center gap-2 transition-colors"
          >
            <Terminal className="w-4 h-4 text-cyan-400" />
            <span>Inspect Python Files & Run Tests</span>
          </button>
        </div>
      </div>

      {/* Security & Privacy Principles */}
      <div className="rounded-2xl bg-[#0f1428]/80 border border-purple-900/30 p-6 space-y-3">
        <div className="flex items-center gap-2 text-sm font-bold text-white">
          <Lock className="w-4 h-4 text-emerald-400" />
          <span>Security, Privacy & Responsible AI Safeguards</span>
        </div>
        <ul className="text-xs text-slate-300 space-y-2 list-disc list-inside leading-relaxed">
          <li><strong>No Hallucinated Credentials:</strong> The AI rewriter converts passive verbs and adds Google XYZ metrics, but strictly places <code>[insert verified metric]</code> when metrics are absent.</li>
          <li><strong>Zero Plaintext Passwords:</strong> Credentials are salted and hashed using 16-byte random salts and PBKDF2-HMAC-SHA256.</li>
          <li><strong>Strict Role & Data Isolation:</strong> Candidate submissions and private recruiter notes are enforced and isolated. Candidates cannot access or modify others' records.</li>
          <li><strong>Advisory Estimations:</strong> Scores are transparent diagnostic aids based on standardized rubrics. Candidates are never auto-rejected by algorithms.</li>
        </ul>
      </div>
    </div>
  );
};
