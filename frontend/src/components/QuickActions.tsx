import React from 'react';
import { ShieldAlert, Building2, CheckCircle2, FileText, Search } from 'lucide-react';

interface QuickActionsProps {
  onSelectAction: (prompt: string) => void;
}

export const QuickActions: React.FC<QuickActionsProps> = ({ onSelectAction }) => {
  const actions = [
    {
      id: 'emergency',
      label: '🚨 Emergency Crisis Help',
      prompt: 'My house was damaged by flooding and we have nowhere to stay.',
      color: 'bg-red-500/10 hover:bg-red-500/20 text-red-400 border-red-500/30',
      icon: ShieldAlert,
    },
    {
      id: 'assistance',
      label: '🏛 Public Assistance',
      prompt: 'I lost my job and my family income is low. What support can I get?',
      color: 'bg-sky-500/10 hover:bg-sky-500/20 text-sky-400 border-sky-500/30',
      icon: Building2,
    },
    {
      id: 'eligibility',
      label: '✓ Check Eligibility Rules',
      prompt: 'Check eligibility for PM-KISAN or low income family assistance.',
      color: 'bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 border-emerald-500/30',
      icon: CheckCircle2,
    },
    {
      id: 'documents',
      label: '📄 Document Checklist',
      prompt: 'What documents do I need to apply for disaster relief housing support?',
      color: 'bg-indigo-500/10 hover:bg-indigo-500/20 text-indigo-400 border-indigo-500/30',
      icon: FileText,
    },
    {
      id: 'service',
      label: '🔎 Find Official Services',
      prompt: 'Where can I find the official portal for social welfare grants in Bihar?',
      color: 'bg-purple-500/10 hover:bg-purple-500/20 text-purple-400 border-purple-500/30',
      icon: Search,
    },
  ];

  return (
    <div className="w-full max-w-5xl mx-auto mb-10 px-4">
      <div className="flex flex-wrap items-center justify-center gap-3">
        {actions.map((action) => (
          <button
            key={action.id}
            onClick={() => onSelectAction(action.prompt)}
            className={`px-4 py-2.5 rounded-2xl border text-xs sm:text-sm font-bold flex items-center gap-2 transition-all cursor-pointer shadow-sm hover:scale-[1.02] ${action.color}`}
          >
            <span>{action.label}</span>
          </button>
        ))}
      </div>
    </div>
  );
};
