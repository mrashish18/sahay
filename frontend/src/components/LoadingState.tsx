import React, { useEffect, useState } from 'react';
import { LifeBuoy, CheckCircle2, Loader2 } from 'lucide-react';

export const LoadingState: React.FC = () => {
  const [stepIndex, setStepIndex] = useState(0);

  const steps = [
    'Understanding your situation & extracting facts...',
    'Searching verified government sources & knowledge base...',
    'Evaluating deterministic eligibility criteria...',
    'Preparing your step-by-step action plan...'
  ];

  useEffect(() => {
    const timer = setInterval(() => {
      setStepIndex((prev) => (prev < steps.length - 1 ? prev + 1 : prev));
    }, 900);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="w-full max-w-xl mx-auto py-16 px-4 text-center space-y-6">
      {/* Animated Brand Icon */}
      <div className="w-14 h-14 mx-auto rounded-3xl bg-gradient-to-tr from-sky-500 via-indigo-500 to-emerald-400 p-[1px] shadow-xl shadow-sky-500/20">
        <div className="w-full h-full bg-[#070B14] rounded-[23px] flex items-center justify-center">
          <LifeBuoy className="w-7 h-7 text-sky-400 animate-spin" />
        </div>
      </div>

      <div>
        <h3 className="text-lg font-black text-white">Sahay is working...</h3>
        <p className="text-xs text-slate-400 mt-1">Analyzing facts & evaluating published criteria</p>
      </div>

      {/* Progressive Steps Checklist */}
      <div className="p-5 rounded-2xl bg-[#0D1422] border border-slate-800 space-y-3 text-left max-w-md mx-auto shadow-inner">
        {steps.map((text, idx) => {
          const isDone = idx < stepIndex;
          const isCurrent = idx === stepIndex;
          return (
            <div key={idx} className="flex items-center gap-3 text-xs">
              {isDone ? (
                <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
              ) : isCurrent ? (
                <Loader2 className="w-4 h-4 text-sky-400 animate-spin flex-shrink-0" />
              ) : (
                <div className="w-4 h-4 rounded-full border border-slate-700 flex-shrink-0" />
              )}
              <span
                className={`font-semibold ${
                  isDone
                    ? 'text-emerald-300'
                    : isCurrent
                    ? 'text-sky-300 font-bold'
                    : 'text-slate-500'
                }`}
              >
                {text}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
};
