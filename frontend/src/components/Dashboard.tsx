import React from 'react';
import { ShieldAlert, Building2, CheckCircle2, FileText, Search } from 'lucide-react';

interface DashboardProps {
  onSelectOption: (promptText: string) => void;
}

export const Dashboard: React.FC<DashboardProps> = ({ onSelectOption }) => {
  const cards = [
    {
      id: 'urgent',
      title: 'I need urgent help',
      description: 'Disaster relief, emergency shelter, food, or safety crisis support.',
      icon: ShieldAlert,
      prompt: 'My house was damaged by flooding and we have nowhere to stay.',
      color: 'from-red-500/20 to-amber-500/10 border-red-500/30 text-red-400',
      badge: '🆘 Crisis Mode'
    },
    {
      id: 'assistance',
      title: 'Find public assistance',
      description: 'Explore financial stipends, unemployment support, and family welfare.',
      icon: Building2,
      prompt: 'I lost my job and my family income is very low. What government support might I qualify for?',
      color: 'from-sky-500/20 to-blue-500/10 border-sky-500/30 text-sky-400',
      badge: '🏛️ Public Welfare'
    },
    {
      id: 'eligibility',
      title: 'Check eligibility',
      description: 'Evaluate structured income, employment, and regional rules.',
      icon: CheckCircle2,
      prompt: 'Check eligibility for low income family assistance program.',
      color: 'from-emerald-500/20 to-teal-500/10 border-emerald-500/30 text-emerald-400',
      badge: '✅ Rule Engine'
    },
    {
      id: 'documents',
      title: 'Understand documents',
      description: 'Find required certificates, proof of income, IDs, and acquisition steps.',
      icon: FileText,
      prompt: 'What documents do I need to apply for unemployment housing support?',
      color: 'from-indigo-500/20 to-violet-500/10 border-indigo-500/30 text-indigo-400',
      badge: '📄 Document Guide'
    },
    {
      id: 'service',
      title: 'Find a service',
      description: 'Search official government portals and verified local issuing authorities.',
      icon: Search,
      prompt: 'Where can I find the official portal for social welfare grants?',
      color: 'from-purple-500/20 to-fuchsia-500/10 border-purple-500/30 text-purple-400',
      badge: '🔎 Service Finder'
    }
  ];

  return (
    <div className="w-full max-w-6xl mx-auto py-8 px-4">
      <div className="text-center mb-10">
        <h2 className="text-3xl font-extrabold text-white tracking-tight sm:text-4xl mb-3">
          How can we help?
        </h2>
        <p className="text-slate-400 max-w-2xl mx-auto text-sm sm:text-base">
          Find the help you need. Know what to do next. Describe your situation naturally or select a category below.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {cards.map((card) => {
          const Icon = card.icon;
          return (
            <button
              key={card.id}
              onClick={() => onSelectOption(card.prompt)}
              className={`glass-card relative text-left p-5 rounded-2xl border bg-gradient-to-br ${card.color} flex flex-col justify-between group hover:scale-[1.02] transition-all duration-200 cursor-pointer shadow-lg`}
            >
              <div>
                <div className="flex items-center justify-between mb-4">
                  <div className="p-3 rounded-xl bg-slate-900/60 border border-white/10 group-hover:border-white/20 transition-all">
                    <Icon className="w-6 h-6" />
                  </div>
                  <span className="text-[11px] font-bold px-2.5 py-1 rounded-full bg-slate-900/70 border border-white/10 text-slate-300">
                    {card.badge}
                  </span>
                </div>
                <h3 className="text-lg font-bold text-white mb-2 group-hover:text-sky-300 transition-colors">
                  {card.title}
                </h3>
                <p className="text-xs text-slate-300 leading-relaxed mb-4">
                  {card.description}
                </p>
              </div>

              <div className="pt-3 border-t border-white/10 flex items-center justify-between text-xs text-slate-400 font-medium">
                <span>Start Navigator</span>
                <span className="text-sky-400 font-semibold group-hover:translate-x-1 transition-transform">→</span>
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
};
