import React from 'react';
import { Cpu, ShieldCheck, CheckCircle2, Award, Search, FileText, AlertTriangle } from 'lucide-react';

interface TechnicalTrustProps {
  onOpenTools: () => void;
}

export const TechnicalTrust: React.FC<TechnicalTrustProps> = ({ onOpenTools }) => {
  const pillars = [
    {
      num: '01',
      title: 'Situation Understanding',
      desc: 'LLM-powered natural language analysis extracts user facts and intent without hallucinating eligibility.',
      icon: Search,
      color: 'text-sky-400 border-sky-500/30 bg-sky-500/10',
    },
    {
      num: '02',
      title: 'Verified Evidence (RAG)',
      desc: 'Jurisdiction-aware vector search retrieves authentic government schemes (.gov.in) with source citations.',
      icon: ShieldCheck,
      color: 'text-emerald-400 border-emerald-500/30 bg-emerald-500/10',
    },
    {
      num: '03',
      title: 'Deterministic Eligibility',
      desc: 'Structured criteria rules evaluate facts deterministically in code. Text generation never decides eligibility.',
      icon: CheckCircle2,
      color: 'text-indigo-400 border-indigo-500/30 bg-indigo-500/10',
    },
    {
      num: '04',
      title: 'Crisis Prioritization',
      desc: 'Emergency displacement and physical safety steps always precede normal welfare guidance.',
      icon: AlertTriangle,
      color: 'text-red-400 border-red-500/30 bg-red-500/10',
    },
  ];

  return (
    <section id="technical-trust" className="w-full max-w-6xl mx-auto py-16 px-4 border-t border-slate-800/80">
      <div className="text-center mb-12">
        <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-400 text-xs font-bold mb-3">
          <Award className="w-4 h-4" />
          <span>WHY SAHAY IS DIFFERENT — TECHNICAL SHOWCASE FOR JUDGES</span>
        </div>
        <h2 className="text-3xl sm:text-4xl font-black text-white">Built for Absolute Public Trust</h2>
        <p className="text-slate-400 max-w-2xl mx-auto text-xs sm:text-sm mt-2">
          Sahay combines conversational AI with non-overridable deterministic execution and sandboxed tool evolution.
        </p>
      </div>

      {/* 4 Pillars Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-10">
        {pillars.map((pillar) => {
          const Icon = pillar.icon;
          return (
            <div key={pillar.num} className="glass-card p-5 rounded-2xl border border-slate-800 space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-2xl font-black text-slate-700">{pillar.num}</span>
                <div className={`p-2.5 rounded-xl border ${pillar.color}`}>
                  <Icon className="w-4 h-4" />
                </div>
              </div>
              <h4 className="text-sm font-bold text-white">{pillar.title}</h4>
              <p className="text-xs text-slate-300 leading-relaxed">{pillar.desc}</p>
            </div>
          );
        })}
      </div>

      {/* Controlled TTE Sandbox Section */}
      <div className="glass-panel p-6 sm:p-8 rounded-3xl space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="p-3 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 text-indigo-400">
              <Cpu className="w-6 h-6" />
            </div>
            <div>
              <h3 className="text-lg font-bold text-white">Controlled Tool Evolution (TTE)</h3>
              <p className="text-xs text-slate-400">Proposal ➔ Static Analysis Linter ➔ Sandbox Verification ➔ Admin Gate</p>
            </div>
          </div>

          <button
            onClick={onOpenTools}
            className="px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold transition-all cursor-pointer shadow-lg shadow-indigo-600/20"
          >
            Inspect TTE Sandbox & Registry
          </button>
        </div>

        <p className="text-xs text-slate-300 leading-relaxed bg-[#070B14] p-4 rounded-2xl border border-slate-800">
          <span className="text-emerald-400 font-bold">✓ Security Guarantee: </span>
          Sahay can propose tool improvements under controlled verification gates. Generated code is never directly executed via eval() or exec() in production.
        </p>
      </div>
    </section>
  );
};
