import React, { useState } from 'react';
import { AlertCircle, RefreshCw, ChevronDown, ChevronUp } from 'lucide-react';

interface ErrorStateProps {
  error: string;
  onRetry: () => void;
}

export const ErrorState: React.FC<ErrorStateProps> = ({ error, onRetry }) => {
  const [showTechDetails, setShowTechDetails] = useState(false);

  return (
    <div className="w-full max-w-xl mx-auto py-16 px-4 text-center space-y-6">
      <div className="w-12 h-12 mx-auto rounded-2xl bg-rose-500/10 border border-rose-500/30 text-rose-400 flex items-center justify-center shadow-lg">
        <AlertCircle className="w-6 h-6" />
      </div>

      <div>
        <h3 className="text-lg font-black text-white">Something went wrong while connecting to Sahay.</h3>
        <p className="text-xs text-slate-400 max-w-md mx-auto mt-1 leading-relaxed">
          The request could not be completed. Please ensure the Sahay backend service is operational and try again.
        </p>
      </div>

      <div className="flex items-center justify-center gap-3">
        <button
          onClick={onRetry}
          className="px-5 py-2.5 bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white rounded-xl text-xs font-bold flex items-center gap-2 shadow-lg shadow-sky-500/20 transition-all cursor-pointer hover:scale-[1.02]"
        >
          <RefreshCw className="w-4 h-4" />
          <span>Try Again</span>
        </button>

        <button
          onClick={() => setShowTechDetails(!showTechDetails)}
          className="px-4 py-2.5 rounded-xl bg-[#0D1422] text-slate-400 hover:text-slate-200 border border-slate-700 text-xs font-semibold flex items-center gap-1.5 transition-colors cursor-pointer"
        >
          <span>{showTechDetails ? 'Hide Technical Details' : 'Technical Details'}</span>
          {showTechDetails ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
        </button>
      </div>

      {showTechDetails && (
        <div className="p-4 rounded-2xl bg-[#0D1422] border border-slate-800 text-left text-xs font-mono text-rose-300 space-y-1 max-w-md mx-auto overflow-x-auto">
          <span className="font-bold text-slate-400">Error Payload / Trace:</span>
          <p className="whitespace-pre-wrap leading-relaxed">{error}</p>
        </div>
      )}
    </div>
  );
};
