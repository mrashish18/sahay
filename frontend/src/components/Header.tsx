import React, { useEffect, useState } from 'react';
import { LifeBuoy, Cpu, Award, ShieldAlert, CheckCircle2, Plus } from 'lucide-react';
import { checkHealth } from '../services/api';

interface HeaderProps {
  onOpenTools: () => void;
  onNavigateHome: () => void;
  onSelectEmergency: () => void;
  onToggleJudgeDrawer: () => void;
  isJudgeDrawerOpen: boolean;
}

export const Header: React.FC<HeaderProps> = ({
  onOpenTools,
  onNavigateHome,
  onSelectEmergency,
  onToggleJudgeDrawer,
  isJudgeDrawerOpen,
}) => {
  const [isHealthy, setIsHealthy] = useState<boolean | null>(null);

  useEffect(() => {
    checkHealth().then((status) => setIsHealthy(status));
  }, []);

  return (
    <header className="sticky top-0 z-40 bg-[#070B14]/85 backdrop-blur-xl border-b border-slate-800/80 px-4 sm:px-6 lg:px-12 py-3.5 flex items-center justify-between transition-all">
      {/* Brand Identity */}
      <button
        onClick={onNavigateHome}
        className="flex items-center gap-3.5 group text-left cursor-pointer focus:outline-none"
      >
        <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-sky-500 via-indigo-500 to-emerald-400 p-[1px] shadow-lg shadow-sky-500/20 group-hover:scale-105 transition-transform">
          <div className="w-full h-full bg-[#070B14] rounded-[15px] flex items-center justify-center">
            <LifeBuoy className="w-5.5 h-5.5 text-sky-400 group-hover:rotate-45 transition-transform duration-300" />
          </div>
        </div>
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-xl font-black tracking-tight text-white group-hover:text-sky-300 transition-colors">
              Sahay
            </h1>
            <span className="text-[10px] uppercase tracking-widest font-black px-2 py-0.5 rounded-md bg-sky-500/10 text-sky-400 border border-sky-500/20">
              CIVIC NAVIGATOR
            </span>
          </div>
          <p className="text-[11px] text-slate-400 font-medium hidden sm:block">
            Public-Service & Crisis Assistance Navigator
          </p>
        </div>
      </button>

      {/* Header Actions */}
      <div className="flex items-center gap-2.5 sm:gap-3">
        {/* New Conversation Button */}
        <button
          onClick={onNavigateHome}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-[#0D1422] hover:bg-slate-800 text-slate-200 border border-slate-700 text-xs font-bold transition-all cursor-pointer shadow-sm"
        >
          <Plus className="w-4 h-4 text-sky-400" />
          <span className="hidden sm:inline">New Conversation</span>
        </button>

        {/* Judge Benchmark Toggle Button */}
        <button
          onClick={onToggleJudgeDrawer}
          className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl border text-xs font-bold transition-all cursor-pointer shadow-sm ${
            isJudgeDrawerOpen
              ? 'bg-amber-500/20 text-amber-300 border-amber-500/40 shadow-amber-500/10'
              : 'bg-[#0D1422] text-amber-400 border-amber-500/30 hover:bg-amber-500/10'
          }`}
        >
          <Award className="w-4 h-4 text-amber-400" />
          <span className="hidden md:inline">Judge Scenarios</span>
        </button>

        {/* Emergency Shortcut Pill */}
        <button
          onClick={onSelectEmergency}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-red-500/10 hover:bg-red-500/20 text-red-400 border border-red-500/30 text-xs font-bold transition-all cursor-pointer shadow-sm"
        >
          <ShieldAlert className="w-4 h-4 text-red-400 animate-pulse" />
          <span className="hidden sm:inline">Crisis Help</span>
        </button>

        {/* Operational Health Badge */}
        {isHealthy !== null && (
          <div
            className={`hidden lg:flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-medium border ${
              isHealthy
                ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
                : 'bg-amber-500/10 text-amber-400 border-amber-500/20'
            }`}
          >
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
            <span>{isHealthy ? 'Engine Operational' : 'Offline Mode'}</span>
          </div>
        )}

        {/* TTE Sandbox Inspector */}
        <button
          onClick={onOpenTools}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-[#0D1422] hover:bg-slate-800 text-slate-300 border border-slate-700 text-xs font-medium transition-colors cursor-pointer"
          title="Inspect Tool Registry & Controlled TTE Sandbox"
        >
          <Cpu className="w-3.5 h-3.5 text-sky-400" />
          <span className="hidden xl:inline">TTE Sandbox</span>
        </button>
      </div>
    </header>
  );
};
