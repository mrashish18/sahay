import React from 'react';
import { Search, ShieldCheck, CheckSquare, Compass } from 'lucide-react';

export const HowItWorks: React.FC = () => {
  const steps = [
    {
      num: '01',
      title: 'Understand Situation',
      desc: 'Sahay analyzes natural language input, classifies crisis urgency, and extracts key user facts.',
      icon: Search,
      color: 'text-sky-400 border-sky-500/30 bg-sky-500/10',
    },
    {
      num: '02',
      title: 'Find Verified Schemes',
      desc: 'Relevant public-service schemes and emergency resources are retrieved via jurisdiction-filtered vector RAG.',
      icon: ShieldCheck,
      color: 'text-emerald-400 border-emerald-500/30 bg-emerald-500/10',
    },
    {
      num: '03',
      title: 'Evaluate Rules',
      desc: 'Structured criteria rules evaluate available facts deterministically without hallucinations or false legal claims.',
      icon: CheckSquare,
      color: 'text-indigo-400 border-indigo-500/30 bg-indigo-500/10',
    },
    {
      num: '04',
      title: 'Actionable Guidance',
      desc: 'Sahay outputs a prioritized step-by-step action plan, document checklist, and official portal links.',
      icon: Compass,
      color: 'text-purple-400 border-purple-500/30 bg-purple-500/10',
    },
  ];

  return (
    <section id="how-it-works" className="w-full max-w-6xl mx-auto py-16 px-4">
      <div className="text-center mb-12">
        <h3 className="text-xs uppercase tracking-widest text-sky-400 font-extrabold mb-2">SYSTEM WORKFLOW</h3>
        <h2 className="text-3xl sm:text-4xl font-extrabold text-white">How Sahay Works</h2>
        <p className="text-slate-400 max-w-2xl mx-auto text-xs sm:text-sm mt-2">
          From natural language input to verified government portal action plan.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
        {steps.map((step) => {
          const Icon = step.icon;
          return (
            <div
              key={step.num}
              className="glass-card p-6 rounded-2xl flex flex-col justify-between border space-y-4"
            >
              <div>
                <div className="flex items-center justify-between mb-4">
                  <span className="text-3xl font-black text-slate-700">{step.num}</span>
                  <div className={`p-3 rounded-xl border ${step.color}`}>
                    <Icon className="w-5 h-5" />
                  </div>
                </div>
                <h4 className="text-base font-bold text-white mb-2">{step.title}</h4>
                <p className="text-xs text-slate-300 leading-relaxed">{step.desc}</p>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
};
