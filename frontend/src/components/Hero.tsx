import React from 'react';
import { Sparkles, Flame, Compass, CheckCircle2, FileText } from 'lucide-react';
import { ChatInput } from './ChatInput';

interface HeroProps {
  onSubmitQuery: (query: string, context?: Record<string, any>) => void;
  isLoading: boolean;
}

export const Hero: React.FC<HeroProps> = ({ onSubmitQuery, isLoading }) => {
  const samplePrompts = [
    {
      icon: Flame,
      category: '🚨 Disaster Relief',
      label: 'Flood Crisis',
      prompt: 'My house was damaged by flooding in Bihar and we have nowhere to stay tonight.',
      context: { country: 'IN', state: 'Bihar' },
      badge: 'Crisis Flow',
      badgeColor: 'border-red-500/30 text-red-400 bg-red-500/10',
    },
    {
      icon: Compass,
      category: '🌾 Public Welfare',
      label: 'Farmer & Family Support',
      prompt: 'I am a low income farmer in Bihar. What government assistance programs can I apply for?',
      context: { country: 'IN', state: 'Bihar' },
      badge: 'Welfare Program',
      badgeColor: 'border-sky-500/30 text-sky-400 bg-sky-500/10',
    },
    {
      icon: CheckCircle2,
      category: '✓ Eligibility Rules',
      label: 'Rule Engine Check',
      prompt: 'Am I eligible for PMAY housing assistance or PM-KISAN income support?',
      context: { country: 'IN', state: 'Bihar' },
      badge: 'Rule Engine',
      badgeColor: 'border-emerald-500/30 text-emerald-400 bg-emerald-500/10',
    },
    {
      icon: FileText,
      category: '📄 Document Guide',
      label: 'Required Documents',
      prompt: 'What documents do I need to apply for disaster emergency housing support?',
      context: { country: 'IN', state: 'Bihar' },
      badge: 'Checklist',
      badgeColor: 'border-indigo-500/30 text-indigo-400 bg-indigo-500/10',
    },
  ];

  return (
    <div className="w-full max-w-4xl mx-auto pt-8 sm:pt-12 pb-8 px-4 text-center space-y-6">
      {/* Top Pill Badge */}
      <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-[#0D1422] border border-slate-800 text-sky-300 text-xs font-bold shadow-sm">
        <Sparkles className="w-4 h-4 text-sky-400 animate-pulse" />
        <span>AI-Powered Public-Service & Crisis Assistance Navigator</span>
      </div>

      {/* Main Headline */}
      <div>
        <h1 className="text-4xl sm:text-6xl font-black text-white tracking-tight mb-2 leading-tight">
          Find the help you need.
        </h1>
        <h2 className="text-3xl sm:text-5xl font-black gradient-text-cyan tracking-tight leading-tight">
          Know what to do next.
        </h2>
      </div>

      {/* Subtitle */}
      <p className="text-slate-300 max-w-xl mx-auto text-xs sm:text-sm leading-relaxed font-normal">
        Tell Sahay what's happening in your own words. We'll help you find relevant public services, understand criteria, and identify the next steps.
      </p>

      {/* Immediate Conversational Chat Input */}
      <div className="pt-2">
        <ChatInput onSubmit={onSubmitQuery} isLoading={isLoading} />
      </div>

      {/* Suggested Prompt Chips Grid */}
      <div className="pt-4 max-w-3xl mx-auto">
        <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400 block mb-3">
          Suggested Questions:
        </span>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 text-left">
          {samplePrompts.map((item, idx) => {
            const Icon = item.icon;
            return (
              <button
                key={idx}
                onClick={() => onSubmitQuery(item.prompt, item.context)}
                className="glass-card p-3 rounded-2xl border border-slate-800 hover:border-sky-500/40 transition-all cursor-pointer group shadow-sm flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-center justify-between mb-1.5">
                    <div className="p-1.5 rounded-lg bg-[#070B14] border border-white/10 text-sky-400 group-hover:text-amber-400 transition-colors">
                      <Icon className="w-3.5 h-3.5" />
                    </div>
                    <span className={`text-[9px] font-extrabold px-1.5 py-0.5 rounded border ${item.badgeColor}`}>
                      {item.badge}
                    </span>
                  </div>
                  <h4 className="text-xs font-bold text-white mb-1 group-hover:text-sky-300 transition-colors">
                    {item.label}
                  </h4>
                  <p className="text-[11px] text-slate-400 leading-snug line-clamp-2">
                    "{item.prompt}"
                  </p>
                </div>

                <div className="pt-2 mt-2 border-t border-slate-800/80 flex items-center justify-between text-[10px] text-slate-400 group-hover:text-sky-400 font-bold transition-colors">
                  <span>Ask Sahay</span>
                  <span>→</span>
                </div>
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
};
