import React from 'react';
import { LifeBuoy } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="w-full border-t border-slate-800/80 bg-[#070C18] py-10 px-6 text-xs text-slate-400">
      <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6 text-center md:text-left">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-xl bg-sky-500/20 text-sky-400 border border-sky-500/30 flex items-center justify-center">
            <LifeBuoy className="w-4 h-4" />
          </div>
          <div>
            <span className="font-extrabold text-white text-sm">Sahay</span>
            <p className="text-[11px] text-slate-400">Public-Service & Crisis Assistance Navigator</p>
          </div>
        </div>

        <div className="flex flex-wrap items-center justify-center gap-6 text-slate-400 font-semibold">
          <span>Verified Sources</span>
          <span>•</span>
          <span>Deterministic Eligibility</span>
          <span>•</span>
          <span>Crisis-Aware Guidance</span>
        </div>

        <div className="text-slate-400">
          © {new Date().getFullYear()} Sahay. Built for public good.
        </div>
      </div>
    </footer>
  );
};
