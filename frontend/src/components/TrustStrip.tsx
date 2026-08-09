import React from 'react';
import { ShieldCheck, MapPin, CheckSquare, AlertTriangle } from 'lucide-react';

export const TrustStrip: React.FC = () => {
  return (
    <div id="verified-sources" className="w-full border-y border-slate-800/80 bg-[#0A0F1D]/80 backdrop-blur-md py-5 px-4 my-10">
      <div className="max-w-6xl mx-auto flex flex-wrap items-center justify-center gap-6 sm:gap-12 text-xs font-bold text-slate-300">
        <div className="flex items-center gap-2">
          <ShieldCheck className="w-4 h-4 text-sky-400" />
          <span>Verified Public Sources (.gov.in)</span>
        </div>
        <span className="text-slate-700 hidden sm:inline">•</span>
        <div className="flex items-center gap-2">
          <MapPin className="w-4 h-4 text-emerald-400" />
          <span>Jurisdiction-Aware Filter</span>
        </div>
        <span className="text-slate-700 hidden sm:inline">•</span>
        <div className="flex items-center gap-2">
          <CheckSquare className="w-4 h-4 text-indigo-400" />
          <span>Deterministic Eligibility Engine</span>
        </div>
        <span className="text-slate-700 hidden sm:inline">•</span>
        <div className="flex items-center gap-2">
          <AlertTriangle className="w-4 h-4 text-red-400" />
          <span>Crisis-Aware Priority Order</span>
        </div>
      </div>
    </div>
  );
};
