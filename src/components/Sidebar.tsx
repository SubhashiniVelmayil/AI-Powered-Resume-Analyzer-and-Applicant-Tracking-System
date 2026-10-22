import React from 'react';
import { 
  LayoutDashboard, 
  FileText, 
  Target, 
  Briefcase, 
  Send, 
  ShieldCheck, 
  UserCircle, 
  Terminal,
  LogOut,
  Sparkles
} from 'lucide-react';
import { UserRole } from '../types';

interface SidebarProps {
  currentTab: string;
  onSelectTab: (tab: string) => void;
  userRole: UserRole;
  userName: string;
  onOpenPythonModal: () => void;
  onLogout: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  currentTab,
  onSelectTab,
  userRole,
  userName,
  onOpenPythonModal,
  onLogout
}) => {
  const navItems = [
    { id: 'dashboard', label: 'Home Dashboard', icon: LayoutDashboard },
    { id: 'resume_analyzer', label: 'Resume Analyzer', icon: FileText },
    { id: 'ats_checker', label: 'ATS Score Checker', icon: Target },
    { id: 'jobs', label: 'Job Recommendations', icon: Briefcase },
    { id: 'applications', label: 'My Applications', icon: Send },
  ];

  if (userRole === 'admin') {
    navItems.push({ id: 'admin', label: 'Admin Dashboard', icon: ShieldCheck });
  }

  navItems.push({ id: 'profile', label: 'Profile & Settings', icon: UserCircle });

  return (
    <aside className="w-64 bg-[#0a0f1d]/95 backdrop-blur-xl border-r border-purple-900/30 flex flex-col justify-between shrink-0 h-screen sticky top-0 text-slate-200 select-none z-20">
      <div>
        {/* App Branding */}
        <div className="p-5 border-b border-purple-900/20">
          <div className="flex items-center gap-2.5">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-cyan-500 via-indigo-500 to-purple-600 flex items-center justify-center shadow-lg shadow-cyan-500/20">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="font-bold text-base bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent leading-none">
                AI Resume ATS
              </h1>
              <p className="text-[11px] text-slate-400 mt-1">Smart Career & Recruiting</p>
            </div>
          </div>
        </div>

        {/* Current User Badge */}
        <div className="px-4 py-3 mx-3 my-3 rounded-xl bg-slate-900/70 border border-slate-800">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-200 truncate max-w-[130px]">{userName}</span>
            <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full uppercase tracking-wider ${
              userRole === 'admin' 
                ? 'bg-purple-500/20 text-purple-300 border border-purple-500/40' 
                : 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40'
            }`}>
              {userRole === 'admin' ? '👑 Admin' : '👤 Candidate'}
            </span>
          </div>
        </div>

        {/* Navigation Items */}
        <nav className="px-3 space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = currentTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => onSelectTab(item.id)}
                className={`w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-xs font-medium transition-all duration-200 ${
                  isActive
                    ? 'bg-gradient-to-r from-cyan-500/15 via-purple-500/15 to-transparent text-cyan-300 border border-cyan-500/30 shadow-sm shadow-cyan-500/10'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? 'text-cyan-400' : 'text-slate-400'}`} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Bottom Footer & Python Project Inspector */}
      <div className="p-3 border-t border-purple-900/20 space-y-2">
        <button
          onClick={onOpenPythonModal}
          className="w-full flex items-center justify-center gap-2 py-2 px-3 rounded-xl bg-purple-950/40 hover:bg-purple-900/40 border border-purple-500/30 text-purple-300 text-xs font-medium transition-colors"
        >
          <Terminal className="w-3.5 h-3.5 text-cyan-400" />
          <span>Python Suite & CLI</span>
        </button>

        <button
          onClick={onLogout}
          className="w-full flex items-center justify-center gap-2 py-2 px-3 rounded-xl text-slate-400 hover:text-rose-400 hover:bg-rose-950/20 text-xs font-medium transition-colors"
        >
          <LogOut className="w-3.5 h-3.5" />
          <span>Sign Out</span>
        </button>
      </div>
    </aside>
  );
};
