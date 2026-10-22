import React from 'react';
import { UserRole } from '../types';
import { Sparkles, Terminal, Shield } from 'lucide-react';

interface NavbarProps {
  title: string;
  subtitle: string;
  userRole: UserRole;
  onToggleRole: () => void;
  onOpenPythonModal: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  title,
  subtitle,
  userRole,
  onToggleRole,
  onOpenPythonModal
}) => {
  return (
    <header className="h-16 border-b border-purple-900/20 bg-[#0c1021]/80 backdrop-blur-md px-6 flex items-center justify-between sticky top-0 z-10">
      <div>
        <h2 className="text-lg font-bold text-white tracking-tight">{title}</h2>
        <p className="text-xs text-slate-400">{subtitle}</p>
      </div>

      <div className="flex items-center gap-3">
        {/* Python Suite launcher */}
        <button
          onClick={onOpenPythonModal}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-800/60 hover:bg-slate-700/60 border border-slate-700 text-slate-300 transition-colors"
          title="Inspect Python files, tests & startup instructions"
        >
          <Terminal className="w-3.5 h-3.5 text-cyan-400" />
          <span>Python Suite</span>
        </button>

        {/* Quick Role Switcher for instant testing */}
        <button
          onClick={onToggleRole}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-gradient-to-r from-purple-600/30 to-indigo-600/30 hover:from-purple-600/40 hover:to-indigo-600/40 border border-purple-500/40 text-purple-200 transition-colors"
          title="Toggle between Candidate and Admin view"
        >
          <Shield className="w-3.5 h-3.5 text-purple-400" />
          <span>Switch to {userRole === 'admin' ? 'Candidate View' : 'Admin View'}</span>
        </button>
      </div>
    </header>
  );
};
