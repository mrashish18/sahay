import React from 'react';
import { HelpCircle } from 'lucide-react';

interface EmptyStateProps {
  onRefine: () => void;
}

export const EmptyState: React.FC<EmptyStateProps> = ({ onRefine }) => {
  return (
    <div className="w-full max-w-xl mx-auto my-8 p-6 sahay-surface rounded-2xl border border-amber-500/30 text-center shadow-xl">
      <div className="w-10 h-10 mx-auto mb-4 rounded-xl bg-amber-500/10 text-amber-400 border border-amber-500/20 flex items-center justify-center">
        <HelpCircle className="w-5 h-5" />
      </div>

      <h3 className="text-base font-bold text-white mb-1">We couldn't find a verified match yet</h3>
      <p className="text-xs text-slate-300 mb-4">We don't want to guess. Try adding specific details to help us find verified assistance:</p>

      <ul className="text-xs text-slate-400 text-left max-w-xs mx-auto space-y-1 mb-6 list-disc list-inside">
        <li>Your state or district (e.g. Bihar, Delhi)</li>
        <li>Specific category of help needed (e.g. food, housing)</li>
        <li>Whether this is an urgent crisis</li>
      </ul>

      <button
        onClick={onRefine}
        className="px-4 py-2 bg-amber-600 hover:bg-amber-500 text-white rounded-xl text-xs font-semibold transition-colors cursor-pointer"
      >
        Refine Your Request
      </button>
    </div>
  );
};
